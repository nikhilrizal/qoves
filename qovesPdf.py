from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class CustomerReportGenerator:
    """ 
    This class represents a simple report generator that counts the words in the text 
    and splits them in half. It then uses a table approach to display them in two columns.
   
    This program is designed for Python 3.10.0 and uses the reportlab==4.1.0 library.
    It has not been tested for other Python versions. 
    
    Thank from nikdevcloud@gmail.com
    """
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.data = """Mirrors lie. They reverse things. That face you see in the bathroom every morning, in your makeup compact: that is “opposite you” — the inverse of the face everyone else sees. We all know this, in theory. And yet, for the past two years or so, this simple fact has riveted and sometimes deeply upset many people (especially young ones) trying out the facial-symmetry filters on social media. Some of these filters invert the mirror’s reflection, revealing images of one’s face as others perceive it, unnerving many users by casting new light on all the imperfections to which our familiar mirrored reflections inure, or even blind us: the uneven hairline, the crooked mouth, the not perfectly level eyes. These all spring sharply into focus when reversed. For these reasons, confronting one’s “flipped” face can feel a bit alienating (not unlike hearing your own voice on tape). Other filters startle in a different way, by creating symmetry, aligning features and smoothing irregularities, or presenting perfected yet"""
        self.doc = SimpleDocTemplate(f"{self.customer_name}p_report.pdf", pagesize=letter)
        self.styles = getSampleStyleSheet() 
        self.font_name = 'DentonTextTest'
        self.font_size = 12
        self.font_path = 'Fonts/Fonts/DentonTextTest-Black.ttf'
        self.register_custom_font() 

    def register_custom_font(self):
        """
            Register the custom font 'DentonTextTest' in TrueType (TTF) format.
            There was an issue working with .otf font, so it has been converted to .ttf.
            For more details, refer to the Stack Overflow post: 
            https://stackoverflow.com/questions/895596/can-anyone-recommend-a-python-pdf-generator-with-opentype-otf-support
        """
        
        pdfmetrics.registerFont(TTFont(self.font_name, self.font_path))
        
    @staticmethod
    def split_paragraph(paragraph):
            """
                Split a paragraph into two halves, ensuring that each half contains approximately
                the same number of words. This function is designed for static pages where long 
                paragraphs need to be evenly distributed across two columns.

                Parameters:
                - paragraph (str): The input paragraph to be split.

                Returns:
                tuple: A tuple containing two strings, each representing one half of the split paragraph.

                Future Improvements:
                - Allow users to specify the desired split ratio.
                - Implement more sophisticated algorithms for even distribution.
                - Handle cases where the input paragraph contains markup or special characters.

                Note: Ensure that the input paragraph is not empty to avoid errors.
            """
        
            if not paragraph:
                return "Error: Empty paragraph"
            words = paragraph.split()
            # Calculate the midpoint to split the paragraph evenly
            midpoint = len(words) // 2
            print(len(words)//2)
            # Join the words for each column
            column1 = ' '.join(words[:midpoint])
            column2 = ' '.join(words[midpoint:])
            return column1, column2


    def generate_report(self):
        """
            Generate a PDF report for the customer using the provided data.

            This method utilizes a two-column layout to display the report content.
            The content includes a title, a spacer for separation, and a table with two columns.

            Example:
            >>> customer_report_instance = CustomerReportGenerator("John_Doe", customer_data)
            >>> customer_report_instance.generate_report()

            Note: Ensure that the 'data' attribute is properly formatted with 'paragraph1' and 'paragraph2'.
      """
        column1, column2 = self.split_paragraph(self.data)
        content = [
            self.get_title(),
            Spacer(1, 12),
            self.create_two_column_table(column1, column2),
        ]

        self.doc.build(content)

    def get_title(self):
        return Paragraph(f"<h> Qoves Report for {self.customer_name}</h>", self.styles["Title"])

    def create_two_column_table(self, text1, text2):
        """
        Create a two-column table with specified text content.

        Parameters:
        - text1 (str): Content for the first column.
        - text2 (str): Content for the second column.

        Returns:
        Table: A ReportLab Table object with two columns.

        Example:
        >>> table_instance = create_two_column_table("Left column content", "Right column content")
        >>> table_instance.drawOn(canvas, x, y)

        Note: Ensure that the text content is properly formatted and does not exceed column widths.
        """
        data = [ [Paragraph(text1, self.get_custom_style()), Paragraph(text2, self.get_custom_style())] ]
        table = Table(data, colWidths=[250, 250], rowHeights=[12])

        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        return table
        
    def get_custom_style(self):

        return ParagraphStyle(
            'CustomStyle',
            parent=self.styles["Normal"],
            fontName=self.font_name,
            fontSize=self.font_size,
        )



if __name__ == '__main__':
    customer_report_instance = CustomerReportGenerator("NikHilRizal")
    customer_report_instance.generate_report()
