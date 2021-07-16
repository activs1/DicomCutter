class DicomSeries:

    def __init__(self, series):
        self.SeriesArray = series
        self.SeriesInstanceUID = self.SeriesArray[0].SeriesInstanceUID
        self.PatientName = self.SeriesArray[0].PatientName
        self.Slices = len(self.SeriesArray)
        self.Rows, self.Columns = self.SeriesArray[0].Rows, self.SeriesArray[0].Columns
        self.PixelSpacing = self.SeriesArray[0].PixelSpacing
        try:
            self.SliceThickness = self.SeriesArray[0].SliceThickness
        except AttributeError:
            self.SliceThickness = 1
        try:
            self.Description = self.SeriesArray[0].SeriesDescription
        except AttributeError:
            self.Description = "no desc"

    def __str__(self):
        pass

    def __eq__(self, other):
        return self.SeriesInstanceUID == other

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < self.Slices:
            value = self.__getitem__(self.i)
            self.i += 1
            return value
        else:
            raise StopIteration

    def __getitem__(self, index):
        try:
            return self.SeriesArray[index]
        except IndexError:
            pass

