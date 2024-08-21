import csv
from typing import List

from django.http import HttpResponse


class CSVHttpResponse(HttpResponse):
    """
    HttpResponse subclass for serving CSV files.

    This class facilitates the creation of a CSV file response in a Django view, automatically setting the appropriate
    headers and writing the CSV content based on provided headers and data.
    """

    content_type: str = 'text/csv'

    def __init__(self, fields: List[str], data: List[dict], filename: str = 'export.csv', *args, **kwargs) -> None:
        """
        Initialize the CSVHttpResponse with headers and data.

        Sets the `Content-Disposition` header to prompt file download with the specified filename, and writes the CSV
        content to the response.

        Args:
            - fields (List[str]): The list of headers for the CSV file.
            - data (List[dict]): The list of dictionaries representing rows of data.
            - filename (str, optional): The name of the file to be downloaded. Defaults to 'export.csv'.
            - *args: Additional positional arguments passed to the parent HttpResponse class.
            - **kwargs: Additional keyword arguments passed to the parent HttpResponse class.
        """
        super().__init__(*args, **kwargs)
        self['Content-Disposition'] = f'attachment; filename="{filename}"'
        self.write_csv_to_response(fields, data)

    def write_csv_to_response(self, headers: List[str], rows: List[dict]) -> None:
        """
        Write CSV headers and rows to the response.

        This method uses the csv.writer to write the provided headers and rows into the HTTP response.

        Args:
            - headers (List[str]): The list of headers for the CSV file.
            - rows (List[dict]): The list of dictionaries representing rows of data.
        """
        writer = csv.writer(self)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(header, '') for header in headers])
