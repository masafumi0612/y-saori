class StatisticsInfo
    def initialize(product_number,product_name,group_name,
        submission_number,submission_average,submission_sum,year)
        #@name = name
        @product_number = []
        @product_name = []
        @group_name = []
        @submission_number = []
        @submission_average = []
        @submission_sum = []
        @year = year
    end

    def product_number()
        @product_number
    end

    def product_name()
        @product_name
    end

    def group_name()
        @group_name
    end

    def submission_number()
        @submission_number
    end

    def submission_average()
        @submission_average
    end

    def submission_sum()
        @submission_sum
    end

    def year()
        @year
    end
end