import analyze as az

class all_covid_data():
    """
    A container for holding all of the analyzed covid data:
    """

    def __init__(self,covid_data):
        self.report_date_list,\
        self.daily_total_list = az.get_daily_totals(covid_data,print_flag=False)

        self.running_total_list = az.get_running_totals(covid_data,print_flag=False)

        self.report_date_list_corr,\
        self.running_total_list_corr = az.fill_data(self.report_date_list,\
                                                    self.running_total_list)
        
        self.report_date_list_back,\
        self.running_tot_list_back = az.fill_backwards(self.report_date_list_corr,\
                                                       self.running_total_list_corr)


        self.facility_list,\
        self.count_per_facility,\
        self.fraction_per_facility = az.bucketize_cases(covid_data,'facility',False)

        self.top_N_facility_list,\
        self.count_per_top_N_facility = az.get_top_shares(self.facility_list,\
                                                          self.count_per_facility,\
                                                          6,
                                                          print_flag=False)

        self.dept_list,\
        self.count_per_dept,\
        self.fraction_per_dept = az.bucketize_cases(covid_data,'dept',False)

        self.top_N_dept_list,\
        self.count_per_top_N_dept = az.get_top_shares(self.dept_list,\
                                                      self.count_per_dept,\
                                                      50,
                                                      print_flag=False)

        self.N_day_avg = 10
        self.N_day_running_avg = az.get_running_average(self.daily_total_list,\
                                                        self.N_day_avg)

        self.N_day_running_avg2 = az.get_running_average(self.running_total_list_corr,10)

        self.sir_data,\
        self.sir_params = az.fit_SIR(self.N_day_running_avg2)

    def print_all_cases(self):
        """Print the total cases at each day."""

        for i in range(len(self.running_tot_list_back)):
            print(self.report_date_list_back[i].strftime("%B %d, %Y"),end="")
            print(" - ",end="")
            print(self.running_tot_list_back[i])

        for j in range(len(self.running_total_list_corr)):
            print(self.report_date_list_corr[j].strftime("%B %d, %Y"),end="")
            print(" - ",end="")
            print(self.running_total_list_corr[j])
    
