import MOSES
import datetime
import putItemIDs_piggybank

import Graphinator

def main():
    while True:
        try:
            print "\n"
            date_string = str(raw_input("Enter a date (YYYY-MM-DD):"))
            print "\n"
            query_date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
            break
        except:
            print "\nPlease enter a valid date."
            

    user_id, password = MOSES.getBigbrotherCredentials()
    MOSES.recursiveUploadRawDataFile(user_id, password)
    putItemIDs_piggybank.main()
    Graphinator.generateDailyGraphs(query_date)


if __name__ == "__main__":
    main()