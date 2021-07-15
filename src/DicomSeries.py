

class DicomSeries:

    def __init__(self, series):
        self.SeriesArray = series
        self.SeriesInstanceUID = self.SeriesArray[0].SeriesInstanceUID
        self.PatientName = self.SeriesArray[0].PatientName
        self.Slices = len(self.SeriesArray)
        self.Rows, self.Columns = self.SeriesArray[0].Rows, self.SeriesArray[0].Columns
        try:
            self.Description = self.SeriesArray[0].SeriesDescription
        except AttributeError:
            self.Description = "no desc"

    def __str__(self):
        pass

    def __eq__(self, other):
        return self.SeriesInstanceUID == other

