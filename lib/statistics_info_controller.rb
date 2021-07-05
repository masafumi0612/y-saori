require 'csv'

require_relative '../lib/statistics_info'

class StatisticsInfoController
    def initialize()

    end

    def print_table(create_single_year_table, create_multiple_years_table, create_graph)
        #creat table html
    end

    def download_table(create_single_year_csv_file, create_multiple_years_csv_file, create_graph)
        #downlod
    end

    def create_single_year_table(product_number,product_name,group_name,
        submission_number,submission_average,submission_sum,year)
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
        label = [""]
        label.concat group_name

        $statistics_year.each_with_index do |i,data|
            table[i].push(data.year)
            table[i].concat data.submission_average
        end
     
        table.unshift label

        return table
    end

    def create_graph(group_name, submission_average, year)

    end

    def create_single_year_csv_file (s_y_table)
        s_y_csv = CSV.generate do |csv|
            s_y_table.each do |data|
                csv << data
            end
        end
        return s_y_csv
    end

    def create_multiple_years_csv_file(m_y_table)
        m_y_csv = CSV.generate do |csv|
            m_y_table.each do |data|
                csv << data
            end
        end
        return m_y_csv
    end

    def push (group="0年度0班", remarks = "0-000-nodata-0")
        gr_sl = group.split("年度")
        rem_sl = remarks.split("-",3)
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
                    data.submission_average.push(1)
                else
                    unless j = data.product_num.find_index{|num|num == gr_sl[1]} then
                        data.product_number.push(rem_sl[1])
                        data.product_name.push(rem_rpar[0])

                        data.submission_number[i].push(1)
                        
                        sum = 0
                        data.submission_number[i].each do |num|
                            sum += num
                        end
                        data.submission_sum[i] = sum

                        ave = data.submission_sum[i] / data.submission_number[i].length
                        data.submission_average[i] = ave
                    else
                        data.submission_number[i][j] += 1
                    end
                end
            end
        end
        return 0
    end
end