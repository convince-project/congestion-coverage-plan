
class Logger:
    def __init__(self, print_time_elapsed=False):
        self.logs = []
        self.print_time_elapsed = print_time_elapsed

    def log(self, message):
        self.logs.append(message)

    def get_logs(self):
        return self.logs


    def save_logs(self, filename):
        with open(filename, 'w') as file:
            for log in self.logs:
                file.write(log + '\n')

    def log_time_elapsed(self, message, time_elapsed):
        if self.print_time_elapsed and time_elapsed is not None and time_elapsed > 0.1:
            print(message, "Time elapsed:", time_elapsed)