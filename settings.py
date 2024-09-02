# Settings dictionary containing configuration parameters for the script

settings = {
    'excel': './fake_names.xlsx',      # Path to the Excel file containing names
    'template': './template.png',      # Path to the certificate template image
    'font': 'Noto.ttf',                # Path to the font file to be used for text
    'output_dir': './certificates/',   # Directory to save generated certificates
    'error_log_file': './errors.log',  # File to log errors during certificate generation
    'font_size': 80,                   # Font size for the text on the certificate
    'max_retries': 3,                  # Maximum number of retries for generating a certificate
    'text_box_width': 500,             # Width of the text box for name placement
    'text_box_height': 100,            # Height of the text box for name placement
    'offset_x': 180,                   # Horizontal offset for text placement
    'offset_y': 100,                   # Vertical offset for text placement
    'keep_singles': False              # Whether to keep individual certificate files after merging into a PDF
}