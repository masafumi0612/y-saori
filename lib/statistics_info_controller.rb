require 'bundler/setup'
require 'csv'
require 'gruff'
require 'rubygems'
require 'zip'
require "fileutils"
require_relative '../lib/statistics_info'

class StatisticsInfoController
    def initialize()

    end

    def print_table(create_single_year_table = "", create_multiple_years_table = "", create_graph = "")
        text = ""

        if create_multiple_years_table
            text << "<h3>&lt;平均提出回数比較表&gt;</h3>"
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
            text << "<h3>&lt;平均提出回数比較グラフ&gt;</h3>"
            text << '<img src="view_graph.cgi">' << "\n"
        end

        if create_single_year_table
            text << "<h3>&lt;提出回数集計表&gt;</h3>"
            create_single_year_table.zip($statistics_year) do |single_year, v|
                text << "<p>#{v.year}年度</p>"
                text << "<table border=1>\n"
                for products in single_year
                    text << "<tr>\n"
                    products.each_with_index do |cell, i|
                        text << "<td>\n"
                        if cell.to_s == "" && i >= 2
                            text << "0"
                        else
                            text << cell.to_s
                        end
                        text << "</td>\n"
                    end
                    text << "</tr>\n"
                end
                text << "</table>\n"
            end
        end


        return text
    end

    def download_table(create_single_year_csv_file, create_multiple_years_csv_file, create_graph)
        input_filenames = create_single_year_csv_file
        if create_multiple_years_csv_file != ""
            input_filenames.push(create_multiple_years_csv_file)
        end
        if create_graph != ""
            input_filenames.push(create_graph)
        end
        download_folder_path = "../downloads/"
        zip_folder_path = "../downloads/"
        zipfile_name = "archive.zip"

        if input_filenames.length == 0
            return ""
        elsif input_filenames.length == 1
            return "#{input_filenames[0]}"
        end

        if File.exist?("#{zip_folder_path}#{zipfile_name}")
            File.delete("#{zip_folder_path}#{zipfile_name}")
        end
        Zip::File.open("#{zip_folder_path}#{zipfile_name}", create: true) do |zipfile|
            input_filenames.each do |filename|
                zipfile.add(filename, File.join(download_folder_path, filename))
            end
        end
        return zipfile_name
    end

    def create_single_year_table(product_number,product_name,group_name,
        submission_number,submission_average,submission_sum,year)
        table = Array.new(product_number.length)

        label = ["成果物通番","成果物名"]
        sort_name = group_name.sort
        g_name = group_name.each_with_index.sort
        label.concat sort_name

        product_number.length.times do |i|
            table[i] = [product_number[i],product_name[i]]
            group_name.length.times do |j|
                table[i].push(submission_number[g_name[j][1]][i])
            end
        end

        botomlabel = ["提出回数平均",""]
        average = []
        submission_average.length.times do |n|
            average.push(submission_average[g_name[n][1]])
        end
        botomlabel.concat average

        table.unshift label
        table.push botomlabel

        return table
    end

    def create_multiple_years_table(group_name,submission_average,years)
        table = Array.new($statistics_year.length)
        label = [""]

        $statistics_year.each_with_index do |data,i|
            sort_name = data.group_name.sort
            g_name = data.group_name.each_with_index.sort

            line = []
            line.push(data.year)
            average = []
            data.group_name.length.times do |n|
                average.push(data.submission_average[g_name[n][1]])
            end
            line.concat average
            table[i] = line
            label = sort_name if label.length < sort_name.length
        end
        label.unshift ""
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

        return 'average.png'
    end

    def create_single_year_csv_file (s_y_table, year)
        s_y_csv = CSV.generate do |csv|
            s_y_table.each do |data|
                csv << data
            end
        end

        File.open("../downloads/#{year}.csv", 'w') do |f|
            f.flock(File::LOCK_EX)
            f.puts s_y_csv
        end
        return "#{year}.csv"
    end

    def create_multiple_years_csv_file(m_y_table)
        m_y_csv = CSV.generate do |csv|
            m_y_table.each do |data|
                csv << data
            end
        end

        File.open("../downloads/multiple_year.csv", 'w') do |f|
            f.flock(File::LOCK_EX)
            f.puts m_y_csv
        end
        return "multiple_year.csv"
    end

    def push (group="0年度0班", remarks = "0-000-nodata-0")
        gr_sl = group.split("年度")
        return 1 if gr_sl[1] == nil
        rem_sl = remarks.split("-",3)
        rem_sl[2] = "split_error" if rem_sl[2] == nil

        rem_rpar = rem_sl[2].rpartition("-")

            $statistics_year.each do |data|
                if data.year == gr_sl[0].to_i then
                    unless i = data.group_name.find_index{|name|name == gr_sl[1]} then
                        i = data.group_name.length
                        data.group_name.push(gr_sl[1])

                        unless j = data.product_number.find_index{|num|num == rem_sl[1]} then
                            j = data.product_number.length
                            data.product_number.push(rem_sl[1])
                            data.product_name.push(rem_rpar[0])
                        end

                        data.submission_number.push([])
                        data.submission_number[i][j] = 1

                        data.submission_sum.push(1)
                        data.submission_average.push(1.0)
                    else
                        unless j = data.product_number.find_index{|num|num == rem_sl[1]} then
                            j = data.product_number.length
                            data.product_number.push(rem_sl[1])
                            data.product_name.push(rem_rpar[0])

                            data.submission_number[i][j] = 1
                        else
                            data.submission_number[i][j] = data.submission_number[i][j].to_i + 1
                        end

                        sum = 0
                        nnum = 0
                        data.submission_number[i].each do |num|
                            unless num == nil then
                                sum += num
                            else
                                nnum += 1
                            end
                        end
                        data.submission_sum[i] = sum

                        ave = (data.submission_sum[i].to_f / (data.submission_number[i].length-nnum).to_f).round(2)
                        data.submission_average[i] = ave
                    end
                end
            end
        return 0
    end
end
