require 'csv'
require 'gruff'
require 'rubygems'
require 'zip'
require_relative '../lib/statistics_info'

class ZipFileGenerator
    # Initialize with the directory to zip and the location of the output archive.
    def initialize(input_dir, output_file)
      @input_dir = input_dir
      @output_file = output_file
    end
    # Zip the input directory.
    def write
      entries = Dir.entries(@input_dir) - %w(. ..)

      ::Zip::File.open(@output_file, ::Zip::File::CREATE) do |io|
        write_entries entries, '', io
      end
    end
    private

    # A helper method to make the recursion work.
    def write_entries(entries, path, io)
      entries.each do |e|
        zip_file_path = path == '' ? e : File.join(path, e)
        disk_file_path = File.join(@input_dir, zip_file_path)
        puts "Deflating #{disk_file_path}"

        if File.directory? disk_file_path
          recursively_deflate_directory(disk_file_path, io, zip_file_path)
        else
          put_into_archive(disk_file_path, io, zip_file_path)
        end
      end
    end

    def recursively_deflate_directory(disk_file_path, io, zip_file_path)
      io.mkdir zip_file_path
      subdir = Dir.entries(disk_file_path) - %w(. ..)
      write_entries subdir, zip_file_path, io
    end

    def put_into_archive(disk_file_path, io, zip_file_path)
      io.get_output_stream(zip_file_path) do |f|
        f.write(File.open(disk_file_path, 'rb').read)
      end
    end
  end

class StatisticsInfoController
    def initialize()

    end

    def print_table(create_single_year_table = "", create_multiple_years_table = "", create_graph = "")
        text = ""

        if create_multiple_years_table
            multiple_year_table_row = create_multiple_years_table[0].length
            text << "<table border=1>\n"
            for single_year in create_multiple_years_table
                text << "<tr>\n"
                for i in 0..(multiple_year_table_row-1)
                    begin
                        text << "<td>\n"
                        text << single_year[i].to_s
                        text << "</td>\n"
                    rescue
                        text << "<td>\n"
                        text << "</td>\n"
                    end
                end
                text << "</tr>\n"
            end
            text << "</table>\n"
        end

        if create_graph != ""
            text << '<img src="../downloads/average.png">' << "\n"
        end

        if create_single_year_table
            for single_year in create_single_year_table
                text << "<table border=1>\n"
                for products in single_year
                    text << "<tr>\n"
                    for cell in products
                        text << "<td>\n"
                        text << cell.to_s
                        text << "</td>\n"
                    end
                    text << "</tr>\n"
                end
                text << "</table>\n"
            end
        end


        return text
        #creat table html
    end

    def download_table(create_single_year_csv_file, create_multiple_years_csv_file, create_graph)
        #downlod
        folder_path = "../downloads"
        zipfile_path = "../archive.zip"

        zip_file_generator = ZipFileGenerator.new(folder_path, zipfile_path)
        zip_file_generator.write

        return zipfile_path
    end

    def create_single_year_table(product_number,product_name,group_name,
        submission_number,submission_average,submission_sum,year)
        table = Array.new(product_number.length)

        label = ["成果物通番","成果物名"]
        label.concat group_name

        product_number.length.times do |i|
            table[i] = [product_number[i],product_name[i]]
            group_name.length.times do |j|
                table[i].push(submission_number[j][i])
            end
        end

        botomlabel = ["提出回数平均",""]
        botomlabel.concat submission_average

        table.unshift label
        table.push botomlabel

        return table
    end

    def create_multiple_years_table(group_name,submission_average,years)
        table = Array.new($statistics_year.length)
        label = [""]
        label.concat group_name

        $statistics_year.each_with_index do |data,i|
            line = []
            line.push(data.year)
            line.concat data.submission_average
            table[i] = line
        end
        table.unshift label
        return table
    end

    def create_graph(group_name, submission_average, year)
        g = Gruff::Bar.new(900)

        g.title = "Average"
        g.x_axis_label = "year"
        g.y_axis_label = "submission_average"
        #g.group_spacing = 3.0
        #g.bar_spacing = 0.7
        #g.legend_box_size  = 10 # => 凡例サイズ
        #g.legend_font_size = 12 # => 凡例のフォントサイズ
        #g.spacing_factor = 1
        #g.bottom_margin = 100
        #g.right_margin = 40
        #g.font = '/Library/Fonts/好きなフォント.ttf'
        #g.show_labels_for_bar_values = true

        #g.legend_margin = 1.0
        g.minimum_value = 0
        g.y_axis_increment = 1.0

        name_data = []
        group_data = []
        $statistics_year.each_with_index do |data,i|
            name_data.push(i,data.year)
            group_data[i] = data.group_name
            group_data[i].each_with_index do |name,i|
                g.data name, submission_average[i]
            end
        end
        g.labels = Hash[*name_data]

        g.write('../downloads/average.png')

        return '../downloads/average.png'
    end

    def create_single_year_csv_file (s_y_table, year)
        s_y_csv = CSV.generate do |csv|
            s_y_table.each do |data|
                csv << data
            end
        end

        File.open("../downloads/#{year}.csv", 'w').puts s_y_csv
        return s_y_csv
    end

    def create_multiple_years_csv_file(m_y_table)
        m_y_csv = CSV.generate do |csv|
            m_y_table.each do |data|
                csv << data
            end
        end

        File.open("../downloads/multiple_year.csv", 'w').puts m_y_csv
        return m_y_csv
    end

    def push (group="0年度0班", remarks = "0-000-nodata-0")
        gr_sl = group.split("年度")
        rem_sl = remarks.split("-",3)
        begin
            rem_rpar = rem_sl[2].rpartition("-")

            $statistics_year.each do |data|
                if data.year == gr_sl[0].to_i then
                    unless i = data.group_name.find_index{|name|name == gr_sl[1]} then
                        data.group_name.push(gr_sl[1])

                        data.product_number.push(rem_sl[1])
                        data.product_name.push(rem_rpar[0])

                        data.submission_number.push([])
                        data.submission_number[data.submission_number.length-1].push(1)

                        data.submission_sum.push(1)
                        data.submission_average.push(1.0)
                    else
                        unless j = data.product_number.find_index{|num|num == rem_sl[1]} then
                            data.product_number.push(rem_sl[1])
                            data.product_name.push(rem_rpar[0])

                            data.submission_number[i].push(1)

                            sum = 0
                            data.submission_number[i].each do |num|
                                sum += num
                            end
                            data.submission_sum[i] = sum

                            ave = (data.submission_sum[i].to_f / data.submission_number[i].length.to_f).round(2)
                            data.submission_average[i] = ave
                        else
                            data.submission_number[i][j] = data.submission_number[i][j].to_i + 1
                            sum = 0
                            data.submission_number[i].each do |num|
                                sum += num
                            end
                            data.submission_sum[i] = sum

                            ave = (data.submission_sum[i].to_f / data.submission_number[i].length.to_f).round(2)
                            data.submission_average[i] = ave
                        end
                    end
                end
            end
        rescue
            return 1
        end
        return 0
    end
end