# quota_pdf.py
import os
from django.conf import settings  # Import the settings module
from django.http import HttpResponse
from django.templatetags.static import (
    static,
)  # Import static to resolve static file URLs
from reportlab.lib import colors
from reportlab.lib.pagesizes import A1, A4, A3, A2  # Use A1 for the page size
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Frame,
    Image,
)
import datetime
import base64
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.platypus import Spacer

left_right_padding = Spacer(
    width=0.75 * inch, height=0
)  # Adjust width for left/right padding
from datetime import datetime
from dateutil import parser  # type: ignore # Import dateutil for better date handling


def format_date(date_str):
    try:
        # Attempt to parse the date
        date_obj = parser.parse(date_str)
        return date_obj.strftime("%B %d, %Y")  # Format to a human-readable string
    except (ValueError, TypeError):
        return "Invalid date"


def safe_string(value, fallback="Not provided"):
    return value or fallback


class QuotaPDF:
    @staticmethod
    def generate_pdf(data, return_type="file", title="Quota Report"):
        if not data:
            return HttpResponse("No data to print", status=400)

        # Get the absolute logo path from static files
        logo_path = os.path.join(
            settings.BASE_DIR, "static/images/logo.png"
        )  # Adjust according to your static file structure
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a buffer to hold the PDF with A1 dimensions
        buffer = BytesIO()
        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A1,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Build the content for the PDF
        content = []

        # Use the Image object for the logo with an absolute path
        logo = Image(logo_path)  # Use the absolute path to the logo
        logo.drawHeight = 100  # Adjust logo size as necessary
        logo.drawWidth = 200  # Adjust logo size as necessary
        content.append(logo)

        # Define styles with appropriate spacing
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name="TitleStyle", fontSize=36, alignment=1, spaceAfter=30
        )  # Increased space after title
        header_style = ParagraphStyle(
            name="HeaderStyle",
            fontSize=12,
            alignment=1,
            textColor=colors.whitesmoke,
            spaceAfter=10,
        )  # Reduced font size for headers
        normal_style = styles["Normal"]  # Default normal style which is smaller

        # Title
        title = Paragraph(title, title_style)
        content.append(title)

        # Table data
        table_data = [
            [
                Paragraph("ID", header_style),
                Paragraph("Name", header_style),
                Paragraph("Scientific Name", header_style),
                Paragraph("No. of Species", header_style),
                Paragraph("Provision Sales", header_style),
                Paragraph("Confirmed", header_style),
                Paragraph("Canceled", header_style),
                Paragraph("Taken", header_style),
            ],
        ]

        for item in data:
            table_data.append(
                [
                    item["id"],
                    item["species"]["name"],
                    item["species"]["scientific_name"],
                    item["quantity"],
                    item["provision_quantity"],
                    item["confirmed_quantity"],
                    item["cancelled_quantity"],
                    item["completed_quantity"],
                ]
            )

        # Create the table with styling
        table = Table(table_data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 5),  # Reduced bottom padding
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("ALTERNATEBACKGROUND", (0, 1), (-1, -1), colors.lavender),
                ]
            )
        )

        content.append(table)

        # Add footer
        footer = f"Created on: {current_datetime}"
        content.append(Paragraph(footer, normal_style))
        content.append(Paragraph("Page 1 of 1", normal_style))

        # Build the PDF
        pdf.build(content)

        # Get the PDF binary data from the buffer
        buffer.seek(0)
        pdf_data = buffer.getvalue()

        if return_type == "base64":
            # Convert to base64 encoding
            encoded_pdf = base64.b64encode(pdf_data).decode("utf-8")
            return {"pdf": encoded_pdf}  # Return a dictionary instead of JsonResponse

        # If return_type is 'file' (default), return as an HTTP response
        return HttpResponse(pdf_data, content_type="application/pdf")


class PriceListPDF:
    @staticmethod
    def generate_pdf(data, return_type="file"):
        if not data:
            return HttpResponse("No data to print", status=400)

        # Get the absolute logo path from static files
        logo_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a buffer to hold the PDF with A1 dimensions
        buffer = BytesIO()
        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A1,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Build the content for the PDF
        content = []

        # Use the Image object for the logo with an absolute path
        logo = Image(logo_path)
        logo.drawHeight = 100  # Adjust logo size as necessary
        logo.drawWidth = 200  # Adjust logo size as necessary
        content.append(logo)

        # Define styles with appropriate spacing
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name="TitleStyle", fontSize=36, alignment=1, spaceAfter=30
        )
        header_style = ParagraphStyle(
            name="HeaderStyle",
            fontSize=12,
            alignment=1,
            textColor=colors.whitesmoke,
            spaceAfter=10,
        )
        normal_style = styles["Normal"]

        # Title
        title = Paragraph("Price List Report", title_style)
        content.append(title)

        # Table data
        header = [
            Paragraph("Package Name", header_style),
            Paragraph("Description", header_style),
            Paragraph("Hunting Type", header_style),  # Added hunting type header
            Paragraph("Price", header_style),
            Paragraph("Currency", header_style),
            Paragraph("Duration", header_style),
            Paragraph("Area", header_style),
        ]

        table_data = [header]  # Start with header

        for item in data:
            price_list = item.get("price_list_type", {})
            sales_package = item.get("sales_package", {})

            row = [
                sales_package.get("name", "N/A"),
                sales_package.get("description", "N/A"),
                price_list.get("hunting_type", {}).get(
                    "name", "N/A"
                ),  # Fetching hunting type for the price list
                price_list.get("amount", "N/A"),
                price_list.get("currency", "N/A"),
                price_list.get("duration", "N/A"),
                price_list.get("price_list", {}).get("area", {}).get("name", "N/A"),
            ]
            table_data.append(row)

        # Create the table with styling
        table = Table(table_data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("ALTERNATEBACKGROUND", (0, 1), (-1, -1), colors.lavender),
                ]
            )
        )

        content.append(table)

        # Add footer
        footer = f"Generated on: {current_datetime}"
        content.append(Paragraph(footer, normal_style))
        content.append(Paragraph("Page 1 of 1", normal_style))

        # Build the PDF
        pdf.build(content)

        # Get the PDF binary data from the buffer
        buffer.seek(0)
        pdf_data = buffer.getvalue()

        if return_type == "base64":
            # Convert to base64 encoding
            encoded_pdf = base64.b64encode(pdf_data).decode("utf-8")
            return {"pdf": encoded_pdf}

        return HttpResponse(pdf_data, content_type="application/pdf")


class SalesConfirmationPDF:
    @staticmethod
    def generate_pdf(salesData, return_type="file"):
        if not salesData:
            return HttpResponse("No data to print", status=400)

        # Paths and initial setup
        logo_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        buffer = BytesIO()
        pdf = SimpleDocTemplate(
            buffer,
            pagesize=A3,
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
            topMargin=1 * inch,
            bottomMargin=1 * inch,
        )

        # Initialize PDF content
        content = []
        styles = getSampleStyleSheet()

        # Logo and Title
        logo = Image(logo_path)
        logo.drawHeight = 50
        logo.drawWidth = 100
        header_table = Table(
            [[logo, Paragraph("<b>SALES CONFIRMATION</b>", styles["Title"])]],
            colWidths=[120, 400],
        )
        header_table.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "CENTER")]))
        content.append(header_table)
        content.append(Paragraph("", styles["Normal"]))  # Spacer

        # Sales Agent and Date
        sales_agent_date = Table(
            [["Sales Agent:", "", "Date:", current_datetime]],
            colWidths=[70, 250, 50, 130],
        )
        sales_agent_date.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ]
            )
        )
        content.append(sales_agent_date)
        content.append(Paragraph("", styles["Normal"]))  # Spacer

        # Client Information
        salesInquiry = salesData.get("sales_inquiry", {})
        salesEntity = salesInquiry.get("entity", {})
        area_name = salesInquiry.get("area", [{}])[0].get("area", {}).get("name", "N/A")

        contacts = salesEntity.get("contacts", [])
        email_contact = contacts[0]["contact"] if len(contacts) > 0 else "N/A"
        phone_contact = contacts[1]["contact"] if len(contacts) > 1 else "N/A"
        address_contact = contacts[2]["contact"] if len(contacts) > 2 else "N/A"

        client_info_data = [
            ["Client Name:", salesEntity.get("full_name", "N/A")],
            ["Address:", address_contact],
            [
                "Home Tel:",
                phone_contact,
                "Work Tel:",
                salesEntity.get("work_tel", "N/A"),
                "Cell:",
                salesEntity.get("cell", "N/A"),
            ],
            ["Email:", email_contact],
            [
                "Type of Hunting Trip:",
                salesData.get("proposed_package", {})
                .get("price_list_type", {})
                .get("hunting_type", {})
                .get("name", "N/A"),
            ],
            ["Hunting Area:", area_name],
            ["Outfitter:", "Bushman Safari Trackers Limited"],
            [
                "Dates:",
                f"{format_date(salesData.get('itinerary', {}).get('arrival', 'N/A'))} - {format_date(salesData.get('itinerary', {}).get('charter_out', 'N/A'))}",
            ],
            ["Details of Trip:", ""],
            ["Price:", ""],
            ["Hunt Combination:", ""],
            ["Companion Hunter / Observer:", ""],
        ]

        col_widths = [150, 200, 60, 120]

        client_info_table = Table(client_info_data, colWidths=col_widths)
        client_info_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        content.append(client_info_table)
        content.append(Paragraph("", styles["Normal"]))  # Spacer

        installments = salesData.get("installments", [])
        if installments:
            installment_data = [
                ["Description", "Amount Due (USD)", "Days", "Due Limit"],
            ]

            total_amount = 0  # Initialize total amount variable

            for installment in installments:
                amount_due = installment.get(
                    "amount_due", "0"
                )  # Default to "0" if not available
                try:
                    amount_due = float(amount_due)  # Convert to float for calculations
                except ValueError:
                    amount_due = 0  # If conversion fails, set to 0

                total_amount += amount_due  # Sum the amounts
                installment_data.append(
                    [
                        installment.get("description", "N/A"),
                        amount_due,
                        installment.get("days", "N/A"),
                        installment.get("due_limit", "N/A"),
                    ]
                )

            # Append total row
            installment_data.append(
                ["Total Amount", total_amount, "", ""]
            )  # Add total line

        else:
            installment_data = [["No installments available", "", "", ""]]

        installment_table = Table(installment_data, colWidths=[200, 150, 100, 150])
        installment_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ]
            )
        )
        content.append(installment_table)
        content.append(Paragraph("", styles["Normal"]))

        # Price Includes and Excludes Sections
        includes_excludes_data = [
            [
                Paragraph("<b>Price includes:</b>", styles["Normal"]),
                Paragraph("<b>Price does not include:</b>", styles["Normal"]),
            ],
            [
                "- Service of experienced professional hunter;",
                "- Trophy fees for animals taken, wounded or lost;",
            ],
            ["- Service of staff;", "- International flights or charter costs;"],
            ["- Camp accommodation;", "- Hotel charges before or after safari;"],
            ["- Daily laundry;", "- Air freight of trophies from Tanzania;"],
            [
                "- Government and concession fees;",
                "- Insurance for trophies being shipped;",
            ],
            ["- 2 Gun Permits;", "- Gratuities, Insurance;"],
            ["- Dip and pack;", "- Entry Visa;"],
            ["- Trophy handling", ""],
        ]

        includes_excludes_table = Table(includes_excludes_data, colWidths=[470, 300])
        includes_excludes_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ]
            )
        )
        content.append(includes_excludes_table)
        content.append(Paragraph("", styles["Normal"]))  # Spacer

        # Notes Section
        note_text = (
            "NOTE: Estimated trophy fees and charter cost will be invoiced prior to the start of the safari. "
            "Trophy fees and charter prices are subject to change at any time by government and charter "
            "companies without notice. Trophy fee deposit is strictly a credit toward trophy fees. "
            "Any difference in trophies taken will be billed or refunded accordingly on the final bill. "
            "CONTRACT IS SUBJECT TO FULL TERMS & CONDITIONS OF BUSHMAN SAFARI TRACKERS LIMITED."
        )
        content.append(Paragraph(note_text, styles["Normal"]))
        content.append(Paragraph("", styles["Normal"]))  # Spacer

        # Signature Section
        signature_table = Table(
            [["Client Signature: ___________________", "Date: ___________________"]],
            colWidths=[490, 200],
        )
        signature_table.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "LEFT")]))
        content.append(signature_table)

        # Footer Note
        footer_note = Paragraph(
            "Please sign, date, and return contract and deposit to our accounting office at: "
            "Bushman Safari Trackers Limited, Plot No. 61-64, Block E, Kihonda Industrial Complex, "
            "P.O. Box 678, Morogoro, Tanzania.",
            styles["Normal"],
        )
        content.append(footer_note)

        # Build PDF and return
        pdf.build(content)
        buffer.seek(0)
        pdf_data = buffer.getvalue()

        if return_type == "base64":
            return {"pdf": base64.b64encode(pdf_data).decode("utf-8")}

        return HttpResponse(pdf_data, content_type="application/pdf")


class SalesInquiryPDF:

    @staticmethod
    def generate_pdf(item, return_type="file"):
        # Create a BytesIO buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=50,
        )
        styles = getSampleStyleSheet()
        logo_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")

        # Custom styles
        header_style = ParagraphStyle(
            "HeaderStyle",
            parent=styles["Heading1"],
            fontSize=20,
            textColor=colors.white,
            backColor=colors.HexColor("#8B4513"),
            alignment=1,
        )
        subheader_style = ParagraphStyle(
            "SubheaderStyle",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#444444"),
        )
        section_header_style = ParagraphStyle(
            "SectionHeaderStyle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#333333"),
            spaceAfter=12,
        )

        # Document content list
        content = []

        # Logo
        # Logo and Title
        logo = Image(logo_path)
        logo.drawHeight = 50
        logo.drawWidth = 100
        content.append(logo)
        content.append(Spacer(1, 10))  # Reduced space after logo

        # Title
        content.append(Paragraph("Sales Inquiry Details", header_style))
        content.append(Spacer(1, 10))

        # Inquiry Code and Created Date
        content.append(
            Paragraph(
                f'Inquiry Code: {safe_string(item["code"])}',
                subheader_style,
            )
        )
        content.append(
            Paragraph(
                f'Created on: {format_date(item["create_date"])}',
                subheader_style,
            )
        )
        content.append(Spacer(1, 10))  # Reduced space

        # Customer Information
        content.append(Paragraph("Customer Information", section_header_style))
        content.append(
            Paragraph(
                f'Full Name: {safe_string(item["entity"].get("full_name"))}',
                styles["Normal"],
            )
        )
        content.append(
            Paragraph(
                f'Nationality: {safe_string(item["entity"].get("nationality", {}).get("name"))}',
                styles["Normal"],
            )
        )
        content.append(
            Paragraph(
                f'Country: {safe_string(item["entity"].get("country", {}).get("name"))}',
                styles["Normal"],
            )
        )
        content.append(Spacer(1, 10))  # Reduced space

        # Contacts
        content.append(Paragraph("Contacts:", styles["Normal"]))
        for contact in item.get("entity", {}).get("contacts", []):
            content.append(Paragraph(f'• {contact.get("contact")}', styles["Normal"]))
        content.append(Spacer(1, 10))  # Reduced space

        # Preference Information
        content.append(Paragraph("Preference Information", section_header_style))
        content.append(
            Paragraph(
                f'Preferred Date: {format_date(item.get("preference", {}).get("preferred_date"))}',
                styles["Normal"],
            )
        )
        content.append(
            Paragraph(
                f'Number of Hunters: {safe_string(item.get("preference", {}).get("no_of_hunters"))}',
                styles["Normal"],
            )
        )
        content.append(
            Paragraph(
                f'Number of Companions: {safe_string(item.get("preference", {}).get("no_of_companions"))}',
                styles["Normal"],
            )
        )
        content.append(
            Paragraph(
                f'Number of Days: {safe_string(item.get("preference", {}).get("no_of_days"))}',
                styles["Normal"],
            )
        )
        content.append(Spacer(1, 10))  # Reduced space

        content.append(Paragraph("Preferred Species", section_header_style))
        preferred_species = item.get("preferred_species", [])

        if preferred_species:
            # Prepare data for the table
            table_data = [["Species Name", "Quantity"]]  # Table Header
            for species in preferred_species:
                table_data.append(
                    [
                        safe_string(species["species"].get("name")),
                        safe_string(species.get("quantity")),
                    ]
                )

            # Create the table
            preferred_species_table = Table(table_data, colWidths=[350, 150])

            # Add style to the table
            preferred_species_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor("#8B4513"),
                        ),  # Header background color
                        (
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            colors.white,
                        ),  # Header text color
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Left align text
                        ("SIZE", (0, 0), (-1, 0), 12),  # Header font size
                        ("SIZE", (0, 1), (-1, -1), 10),  # Data font size
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Grid lines
                    ]
                )
            )

            # Add the table to the content
            content.append(preferred_species_table)
        else:
            content.append(Paragraph("No preferred species listed.", styles["Normal"]))

        content.append(Spacer(1, 10))  # Reduced space

        # Area Information
        content.append(Paragraph("Area Information", section_header_style))
        area_info = item.get("area", [])
        if area_info:
            for area in area_info:
                content.append(
                    Paragraph(
                        f'Area ID: {safe_string(area.get("id"))}, Area: {safe_string(area.get("area", {}).get("name", "Unnamed"))}',
                        styles["Normal"],
                    )
                )
        else:
            content.append(
                Paragraph("No area information available.", styles["Normal"])
            )
        content.append(Spacer(1, 10))  # Reduced space

        # Remarks
        content.append(Paragraph("Remarks", section_header_style))
        content.append(
            Paragraph(
                safe_string(item.get("remarks"), "No remarks provided."),
                styles["Normal"],
            )
        )
        content.append(Spacer(1, 10))  # Reduced space

        # Build PDF
        doc.build(content)

        # Seek to the beginning of the buffer so we can read its content
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()

        if return_type == "base64":
            return {"pdf": base64.b64encode(pdf_data).decode("utf-8")}

        return HttpResponse(pdf_data, content_type="application/pdf")


class SalesContractPDF:
    @staticmethod
    def generate_pdf(salesData, return_type="file"):
        if not salesData:
            return HttpResponse("No data to print", status=400)

        # Log salesData for debugging

        # Paths and initial setup
        logo_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=50,
            bottomMargin=40,
        )
        styles = getSampleStyleSheet()

        # Define custom styles using the previous color scheme
        header_style = ParagraphStyle(
            "HeaderStyle",
            parent=styles["Heading1"],
            fontSize=26,
            textColor=colors.white,
            backColor=colors.HexColor("#8B4513"),
            alignment=1,
            spaceAfter=12,
        )

        subheader_style = ParagraphStyle(
            "SubheaderStyle",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#4B0082"),
            spaceAfter=6,
        )

        normal_style = styles["Normal"]
        normal_style.fontSize = 12
        normal_style.leading = 14

        # Create content list
        content = []

        # Insert Logo
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            logo.drawHeight = 60
            logo.drawWidth = 120
            content.append(logo)
            content.append(Spacer(1, 12))

        # Title
        content.append(Paragraph("Sales Contract", header_style))
        content.append(Spacer(1, 20))

        # Contract Details Section
        content.append(Paragraph("Contract Details", subheader_style))
        content.append(Spacer(1, 6))

        # Detail Fields
        fields = [
            f"Contract Number: <b>{salesData.get('contract_number', 'N/A')}</b>",
            f"Start Date: <b>{salesData.get('start_date', 'N/A')}</b>",
            f"End Date: <b>{salesData.get('end_date', 'N/A')}</b>",
            f"Description: <i>{salesData.get('description', 'N/A')}</i>",
            f"Created At: {salesData.get('created_at', 'N/A')}",
            f"Updated At: {salesData.get('updated_at', 'N/A')}",
        ]
        for field in fields:
            content.append(Paragraph(field, normal_style))
        content.append(Spacer(1, 12))

        # Sales Confirmation Proposal ID
        proposal_id = salesData.get("sales_confirmation_proposal", {}).get("id", "N/A")
        content.append(
            Paragraph(
                f"Sales Confirmation Proposal ID: <b>{proposal_id}</b>", normal_style
            )
        )

        # Client Information Section
        content.append(Spacer(1, 12))
        content.append(Paragraph("Client Information", subheader_style))
        content.append(Spacer(1, 6))

        # Accessing the entity from the sales proposal
        entity = (
            salesData.get("sales_confirmation_proposal", {})
            .get("sales_inquiry", {})
            .get("entity", {})
        )

        content.append(
            Paragraph(f"Entity ID: <b>{entity.get('id', 'N/A')}</b>", normal_style)
        )
        content.append(
            Paragraph(
                f"Entity Name: <b>{entity.get('full_name', 'N/A')}</b>", normal_style
            )
        )
        content.append(
            Paragraph(
                f"Nationality: <b>{entity.get('nationality', {}).get('name', 'N/A')}</b>",
                normal_style,
            )
        )
        content.append(
            Paragraph(
                f"Country: <b>{entity.get('country', {}).get('name', 'N/A')}</b>",
                normal_style,
            )
        )

        # Contact Details Section
        content.append(Spacer(1, 12))
        content.append(Paragraph("Contact Details:", subheader_style))
        for contact in entity.get("contacts", []):
            content.append(Paragraph(f"• {contact.get('contact')}", normal_style))

        # Sales Inquiry Details Section
        sales_inquiry = salesData.get("sales_confirmation_proposal", {}).get(
            "sales_inquiry", {}
        )
        content.append(Spacer(1, 12))
        content.append(Paragraph("Sales Inquiry Details", subheader_style))
        content.append(Spacer(1, 6))

        inquiry_fields = [
            f"Preferred Date: <b>{sales_inquiry.get('preference', {}).get('preferred_date', 'N/A')}</b>",
            f"No of Hunters: <b>{sales_inquiry.get('preference', {}).get('no_of_hunters', 'N/A')}</b>",
            f"No of Companions: <b>{sales_inquiry.get('preference', {}).get('no_of_companions', 'N/A')}</b>",
            (
                f"Preferred Species: <b>{sales_inquiry.get('preferred_species', [{}])[0].get('species', {}).get('name', 'N/A')}</b>"
                if sales_inquiry.get("preferred_species")
                else "None"
            ),
        ]
        for field in inquiry_fields:
            content.append(Paragraph(field, normal_style))

        # Price Breakdown Section
        price_breakdown = salesData.get("sales_confirmation_proposal", {}).get(
            "price_break_down", {}
        )
        content.append(Spacer(1, 12))
        content.append(Paragraph("Price Breakdown", subheader_style))
        content.append(Spacer(1, 6))

        price_fields = [
            f"Total Amount: <b>{price_breakdown.get('total_amount', {}).get('currency', {}).get('symbol', '')} "
            f"{price_breakdown.get('total_amount', {}).get('amount', 'N/A')}</b>",
        ]

        if "companion_cost_details" in price_breakdown:
            companion_cost = price_breakdown["companion_cost_details"]
            number_of_companions = companion_cost.get("number_of_companions", "N/A")
            cost_per_companion = companion_cost.get("cost_per_companion", {})
            cost_per_companion_amount = f"{cost_per_companion.get('currency', {}).get('symbol', '')} {cost_per_companion.get('amount', 'N/A')}"

            price_fields.append(f"Number of Companions: <b>{number_of_companions}</b>")
            price_fields.append(
                f"Cost per Companion: <b>{cost_per_companion_amount}</b>"
            )
        else:
            price_fields.append("<b>Companion Cost Details: Not Available</b>")

        for field in price_fields:
            content.append(Paragraph(field, normal_style))

        # Final Touches: Add Footer with Company Details
        content.append(Spacer(1, 20))
        content.append(Paragraph("Thank you for choosing us!", normal_style))
        content.append(
            Paragraph(
                "For any inquiries, please contact us at: info@yourcompany.com",
                normal_style,
            )
        )
        content.append(Paragraph("Company Name | Address | Phone Number", normal_style))

        # Build the document
        doc.build(content)

        # Get the PDF binary data from the buffer
        buffer.seek(0)
        pdf_data = buffer.getvalue()

        if return_type == "base64":
            return {"pdf": base64.b64encode(pdf_data).decode("utf-8")}

        return HttpResponse(pdf_data, content_type="application/pdf")


class PermitPDF:
    @staticmethod
    def generate_pdf(permit_data, return_type="file"):
        # Create a BytesIO buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()

        # Custom styles
        header_style = ParagraphStyle(
            "HeaderStyle",
            parent=styles["Heading1"],
            fontSize=20,
            textColor=colors.white,
            backColor=colors.HexColor("#8B4513"),
            alignment=1,
        )
        subheader_style = ParagraphStyle(
            "SubheaderStyle",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#444444"),
        )
        section_header_style = ParagraphStyle(
            "SectionHeaderStyle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#333333"),
            spaceAfter=12,
        )

        # Create a list to hold the content
        content = []

        # Add Permit details
        content.append(Paragraph("Permit Details", header_style))
        content.append(Spacer(1, 12))

        content.append(
            Paragraph(f"Permit Number: {permit_data['permit_number']}", subheader_style)
        )
        content.append(
            Paragraph(f"Issued Date: {permit_data['issued_date']}", subheader_style)
        )
        content.append(
            Paragraph(f"Description: {permit_data['description']}", subheader_style)
        )
        content.append(
            Paragraph(f"Created At: {permit_data['created_at']}", subheader_style)
        )
        content.append(
            Paragraph(f"Updated At: {permit_data['updated_at']}", subheader_style)
        )
        content.append(Spacer(1, 12))

        content.append(
            Paragraph(
                f"Entity Contract ID: {permit_data['entity_contract']}", subheader_style
            )
        )
        content.append(
            Paragraph(
                f"Package Type ID: {permit_data['package_type']}", subheader_style
            )
        )
        content.append(Spacer(1, 12))

        # Add Dates Information
        content.append(Paragraph("Dates", section_header_style))

        if permit_data.get("dates"):
            for date_info in permit_data["dates"]:
                content.append(
                    Paragraph(
                        f"Start Date: {date_info['start_date']}", styles["Normal"]
                    )
                )
                content.append(
                    Paragraph(f"End Date: {date_info['end_date']}", styles["Normal"])
                )
                content.append(
                    Paragraph(
                        f"Created At: {date_info['created_at']}", styles["Normal"]
                    )
                )
                content.append(
                    Paragraph(
                        f"Updated At: {date_info['updated_at']}", styles["Normal"]
                    )
                )
                content.append(
                    Paragraph(
                        f"Entity Contract Permit ID: {date_info['entity_contract_permit']}",
                        styles["Normal"],
                    )
                )
                # Update this part to showcase if amendment is null
                amendment_text = (
                    f"Amendment: {date_info['amendment']}"
                    if date_info["amendment"] is not None
                    else "Amendment: Not updated"
                )
                content.append(Paragraph(amendment_text, styles["Normal"]))
                content.append(Spacer(1, 12))
        else:
            content.append(
                Paragraph("No date information available.", styles["Normal"])
            )

        # Build the document
        doc.build(content)

        # Seek to the beginning of the buffer so we can read its content
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()

        if return_type == "base64":
            return {"pdf": base64.b64encode(pdf_data).decode("utf-8")}

        return HttpResponse(pdf_data, content_type="application/pdf")


class GamePDF:

    @staticmethod
    def generate_pdf(game_data, return_type="file"):
        buffer = BytesIO()
        # Creating a SimpleDocTemplate with margin settings
        margin = 50  # Adjust margin as required
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A2,
            rightMargin=margin,
            leftMargin=margin,
            topMargin=margin,
            bottomMargin=margin,
        )
        styles = getSampleStyleSheet()

        # Load the logo for the PDF
        logo_path = os.path.join(settings.BASE_DIR, "static/images/logo.png")

        # Custom styles for the PDF
        header_style = styles["Heading1"]
        header_style.fontSize = 24
        header_style.textColor = colors.white
        header_style.backColor = colors.HexColor("#8B4513")
        header_style.alignment = 1

        subheader_style = styles["Heading2"]
        subheader_style.fontSize = 18
        subheader_style.textColor = colors.HexColor("#444444")

        section_header_style = styles["Heading2"]
        section_header_style.fontSize = 16
        section_header_style.textColor = colors.HexColor("#333333")
        section_header_style.spaceAfter = 12

        # Create content list
        content = []

        # Add Permit Information and Logo
        permit = game_data["entity_contract_permit"]
        permit_info = Paragraph(
            f"PERMIT NO: {permit['permit_number']}", styles["Normal"]
        )
        content.append(permit_info)
        content.append(Spacer(1, 12))

        # ** Add Logo Next to Permit Information **

        client = game_data["client"]
        content.append(
            Paragraph(f"CLIENT NAME: {client['full_name']}", styles["Normal"])
        )
        content.append(
            Paragraph("COMPANY NAME: BUSHMAN HUNTING SAFARI (T) LTD", styles["Normal"])
        )

        ph_list = game_data.get("ph", [])
        if ph_list:
            ph = ph_list[0]["ph"]  # Use the first PH entry as an example
            content.append(
                Paragraph(f"PH NAME: {ph['full_name']}", styles["Normal"])
            )  # Ensure full_name exists
            content.append(
                Paragraph(
                    f"PH LICENCE NO: {ph.get('licence_number', 'N/A')}",
                    styles["Normal"],
                )
            )
        else:
            content.append(Paragraph("PH NAME: N/A", styles["Normal"]))
            content.append(Paragraph("PH LICENCE NO: N/A", styles["Normal"]))
        content.append(Spacer(1, 12))

        # Add Species Table
        species_data = [
            [
                "S/N",
                "SPECIES",
                "QUANTITY",
                "AREA",
                "WEAPONS USED",
                "DATE",
                "TIME",
                "SEX",
                "GPS COORDINATES",
                "REMARKS",
            ]
        ]
        for entry in game_data.get("game_killed_activity", []):
            lat = entry["location"]["geo_coordinates"]["coordinates"][0]["lat"]
            lng = entry["location"]["geo_coordinates"]["coordinates"][0]["lng"]
            coordinates = f"{lat}, {lng}"
            species_data.append(
                [
                    entry["id"],
                    entry["species"]["name"],
                    entry["quantity"],
                    entry.get("area", {}).get(
                        "name", "Unknown"
                    ),  # Assuming area has a 'name'
                    entry.get("weapon_used", "N/A"),
                    entry["date"],
                    entry["time"],
                    entry.get(
                        "spacies_gender", "N/A"
                    ),  # Assuming species gender is represented this way
                    coordinates,
                    entry.get("status", "No remarks"),
                ]
            )

        # Calculate column widths based on maximum length of each column data
        col_widths = GamePDF.calculate_column_widths(species_data)

        # Create the table with calculated column widths
        table = Table(species_data, colWidths=col_widths, hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), "#8B4513"),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Ensure left alignment
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        content.append(table)

        GamePDF.signature_table(content, doc, styles)

        # declaration

        declaration_text = "We, the above signed persons  hereby daclare  that the register of th animal hunted  including wounded  is a record of all  animals killed or wounded durig the validity of the huntig permit"
        # append declaration_data to content
        content.append(Spacer(1, 12))
        # make bold
        content.append(Paragraph("DECLARATION", styles["Normal"]))

        content.append(Spacer(1, 12))
        # not intable
        # content.append(Table(declaration_data, colWidths=[doc.width/2]))
        content.append(Paragraph(declaration_text, styles["Normal"]))

        # Add Signatures text below the line of dots

        GamePDF.signature_table(content, doc, styles)

        # Build the PDF document
        doc.build(content)

        # Seek to the beginning of the buffer
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()

        # Return the PDF data
        if return_type == "base64":
            return {"pdf": base64.b64encode(pdf_data).decode("utf-8")}
        return HttpResponse(pdf_data, content_type="application/pdf")

    @staticmethod
    def signature_table(content, doc, styles):  # Signature Dotted Lines Table
        signature_doted_line = [
            "..................................................................",
            ".................................................................",
            "..................................................................",
        ]

        # Create a table for the dotted lines
        signature_table = Table(
            [
                signature_doted_line
            ],  # We put the signature_doted_line inside another list to create one row
            colWidths=[doc.width / 3] * 3,  # Equal width for each column
        )
        signature_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Center the dotted lines
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0,
                        colors.transparent,
                    ),  # No gridlines for dotted lines
                ]
            )
        )
        content.append(Spacer(1, 20))  # Add some space before the table
        content.append(signature_table)

        # Prepare Signature Labels Below the Table
        signature_labels = [
            "SIGNATURE OF THE HUNTING CLIENT",
            "SIGNATURE OF PROFESSIONAL HUNTER",
            "SIGNATURE OF WILDLIFE OFFICER IN CHARGE",
        ]

        signature_label_data = [
            [Paragraph(label, styles["Normal"]) for label in signature_labels]
        ]

        # Create a table for signatures
        signature_labels_table = Table(
            signature_label_data,
            colWidths=[doc.width / 3] * 3,  # Equal width for each column
        )
        signature_labels_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center the labels
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0,
                        colors.transparent,
                    ),  # No gridlines for the signature section
                ]
            )
        )

        content.append(signature_labels_table)

    @staticmethod
    def calculate_column_widths(data):
        """Calculate column widths based on the maximum content length."""
        max_lengths = [max(len(str(item)) for item in col) for col in zip(*data)]
        # Adjust the width (in points) you want for the column based on your preference
        adjusted_widths = [
            (length * 7) + 30 for length in max_lengths
        ]  # 7 is a rough estimate per character
        return adjusted_widths
