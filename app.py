import json
import pycountry
import phonenumbers
from phonenumbers import geocoder, carrier
from tkinter import Tk, Label, Button, Entry, Frame, messagebox, PhotoImage
from tkinter import ttk
import tkinter.font as tkFont
from phone_iso3166.country import phone_country


class PhoneTracker:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_styles()
        self.create_widgets()
        self.setup_animations()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("📱 Advanced Phone Number Tracker")
        self.root.geometry("600x700")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"600x700+{x}+{y}")
        
    def create_styles(self):
        """Create custom styles for ttk widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure button style
        self.style.configure(
            "Custom.TButton",
            background="#00d4aa",
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            font=("Arial", 12, "bold")
        )
        
        self.style.map(
            "Custom.TButton",
            background=[("active", "#00b894"), ("pressed", "#00a085")]
        )
        
    def create_widgets(self):
        """Create and place all widgets"""
        # Header Frame
        header_frame = Frame(self.root, bg="#1a1a2e", height=120)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        # Title
        title_font = tkFont.Font(family="Arial", size=28, weight="bold")
        title_label = Label(
            header_frame,
            text="📱 Phone Tracker",
            font=title_font,
            bg="#1a1a2e",
            fg="#00d4aa"
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_font = tkFont.Font(family="Arial", size=12)
        subtitle_label = Label(
            header_frame,
            text="Discover the origin of any phone number",
            font=subtitle_font,
            bg="#1a1a2e",
            fg="#a0a0a0"
        )
        subtitle_label.pack()
        
        # Input Frame
        input_frame = Frame(self.root, bg="#16213e", relief="raised", bd=2)
        input_frame.pack(fill="x", padx=40, pady=20, ipady=30)
        
        # Phone number input section
        input_label = Label(
            input_frame,
            text="Enter Phone Number:",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="white"
        )
        input_label.pack(pady=(20, 10))
        
        # Entry with custom styling
        entry_frame = Frame(input_frame, bg="#16213e")
        entry_frame.pack(pady=10)
        
        self.phone_entry = Entry(
            entry_frame,
            width=25,
            font=("Arial", 16),
            bg="#2c3e50",
            fg="white",
            relief="flat",
            bd=10,
            insertbackground="white",
            justify="center"
        )
        self.phone_entry.pack(ipady=8, ipadx=10)
        
        # Example text
        example_label = Label(
            input_frame,
            text="Example: +1234567890 or +919876543210",
            font=("Arial", 10),
            bg="#16213e",
            fg="#7f8c8d"
        )
        example_label.pack(pady=(5, 0))
        
        # Buttons Frame
        button_frame = Frame(input_frame, bg="#16213e")
        button_frame.pack(pady=20)
        
        # Track button with custom styling
        self.track_btn = Button(
            button_frame,
            text="🔍 Track Location",
            font=("Arial", 14, "bold"),
            bg="#00d4aa",
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.track_phone_number
        )
        self.track_btn.pack(side="left", padx=10)
        
        # Clear button
        self.clear_btn = Button(
            button_frame,
            text="🗑️ Clear",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.clear_fields
        )
        self.clear_btn.pack(side="left", padx=10)
        
        # Results Frame
        self.results_frame = Frame(self.root, bg="#0f1419", relief="raised", bd=2)
        self.results_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Results Title
        results_title = Label(
            self.results_frame,
            text="📊 Results",
            font=("Arial", 18, "bold"),
            bg="#0f1419",
            fg="#00d4aa"
        )
        results_title.pack(pady=(20, 10))
        
        # Results display area
        self.create_result_fields()
        
        # Status bar
        self.status_var = Label(
            self.root,
            text="Ready to track phone numbers",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            relief="sunken",
            bd=1
        )
        self.status_var.pack(fill="x", side="bottom")
        
        # Bind Enter key to track function
        self.phone_entry.bind('<Return>', lambda event: self.track_phone_number())
        
    def create_result_fields(self):
        """Create result display fields"""
        # Country
        self.country_frame = Frame(self.results_frame, bg="#0f1419")
        self.country_frame.pack(fill="x", padx=20, pady=10)
        
        Label(self.country_frame, text="🌍 Country:", font=("Arial", 12, "bold"), 
              bg="#0f1419", fg="#3498db").pack(anchor="w")
        self.country_label = Label(self.country_frame, text="Not tracked yet", 
                                 font=("Arial", 14), bg="#0f1419", fg="white", wraplength=500)
        self.country_label.pack(anchor="w", padx=20)
        
        # Region/State
        self.region_frame = Frame(self.results_frame, bg="#0f1419")
        self.region_frame.pack(fill="x", padx=20, pady=10)
        
        Label(self.region_frame, text="📍 Region:", font=("Arial", 12, "bold"), 
              bg="#0f1419", fg="#e67e22").pack(anchor="w")
        self.region_label = Label(self.region_frame, text="Not tracked yet", 
                                font=("Arial", 14), bg="#0f1419", fg="white", wraplength=500)
        self.region_label.pack(anchor="w", padx=20)
        
        # Carrier
        self.carrier_frame = Frame(self.results_frame, bg="#0f1419")
        self.carrier_frame.pack(fill="x", padx=20, pady=10)
        
        Label(self.carrier_frame, text="📱 Carrier:", font=("Arial", 12, "bold"), 
              bg="#0f1419", fg="#9b59b6").pack(anchor="w")
        self.carrier_label = Label(self.carrier_frame, text="Not tracked yet", 
                                 font=("Arial", 14), bg="#0f1419", fg="white", wraplength=500)
        self.carrier_label.pack(anchor="w", padx=20)
        
        # Number Type
        self.type_frame = Frame(self.results_frame, bg="#0f1419")
        self.type_frame.pack(fill="x", padx=20, pady=10)
        
        Label(self.type_frame, text="📞 Number Type:", font=("Arial", 12, "bold"), 
              bg="#0f1419", fg="#1abc9c").pack(anchor="w")
        self.type_label = Label(self.type_frame, text="Not tracked yet", 
                              font=("Arial", 14), bg="#0f1419", fg="white", wraplength=500)
        self.type_label.pack(anchor="w", padx=20)
        
    def setup_animations(self):
        """Setup hover effects for buttons"""
        def on_enter(e, btn, color):
            btn.configure(bg=color)
            
        def on_leave(e, btn, color):
            btn.configure(bg=color)
            
        # Track button hover effect
        self.track_btn.bind("<Enter>", lambda e: on_enter(e, self.track_btn, "#00b894"))
        self.track_btn.bind("<Leave>", lambda e: on_leave(e, self.track_btn, "#00d4aa"))
        
        # Clear button hover effect
        self.clear_btn.bind("<Enter>", lambda e: on_enter(e, self.clear_btn, "#c0392b"))
        self.clear_btn.bind("<Leave>", lambda e: on_leave(e, self.clear_btn, "#e74c3c"))
        
    def track_phone_number(self):
        """Enhanced phone number tracking with multiple information sources"""
        phone_number = self.phone_entry.get().strip()
        
        if not phone_number:
            messagebox.showwarning("Input Error", "Please enter a phone number!")
            return
            
        self.status_var.config(text="Tracking phone number...")
        self.root.update()
        
        try:
            # Parse the phone number using phonenumbers library
            parsed_number = phonenumbers.parse(phone_number, None)
            
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError("Invalid phone number format")
            
            # Get country information
            country_code = f"+{parsed_number.country_code}"
            country_alpha2 = phone_country(phone_number)
            
            if country_alpha2:
                country_info = pycountry.countries.get(alpha_2=country_alpha2)
                if country_info:
                    country_name = getattr(country_info, 'official_name', country_info.name)
                    country_display = f"{country_name} ({country_code})"
                else:
                    country_display = f"Unknown Country ({country_code})"
            else:
                country_display = f"Unknown Country ({country_code})"
            
            # Get location information
            location = geocoder.description_for_number(parsed_number, "en")
            if not location:
                location = "Location information not available"
            
            # Get carrier information
            carrier_name = carrier.name_for_number(parsed_number, "en")
            if not carrier_name:
                carrier_name = "Carrier information not available"
            
            # Get number type
            number_type = phonenumbers.number_type(parsed_number)
            type_mapping = {
                phonenumbers.PhoneNumberType.MOBILE: "Mobile",
                phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
                phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
                phonenumbers.PhoneNumberType.TOLL_FREE: "Toll Free",
                phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
                phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
                phonenumbers.PhoneNumberType.VOIP: "VoIP",
                phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
                phonenumbers.PhoneNumberType.PAGER: "Pager",
                phonenumbers.PhoneNumberType.UAN: "Universal Access Number",
                phonenumbers.PhoneNumberType.VOICEMAIL: "Voicemail"
            }
            
            number_type_str = type_mapping.get(number_type, "Unknown")
            
            # Update the display
            self.country_label.config(text=country_display)
            self.region_label.config(text=location)
            self.carrier_label.config(text=carrier_name)
            self.type_label.config(text=number_type_str)
            
            self.status_var.config(text="Tracking completed successfully!")
            
        except Exception as e:
            error_msg = f"Error tracking number: {str(e)}"
            messagebox.showerror("Tracking Error", error_msg)
            self.status_var.config(text="Tracking failed")
            
            # Clear results on error
            self.clear_results()
    
    def clear_fields(self):
        """Clear all input and result fields"""
        self.phone_entry.delete(0, 'end')
        self.clear_results()
        self.status_var.config(text="Fields cleared - Ready for new search")
        
    def clear_results(self):
        """Clear only result fields"""
        self.country_label.config(text="Not tracked yet")
        self.region_label.config(text="Not tracked yet")
        self.carrier_label.config(text="Not tracked yet")
        self.type_label.config(text="Not tracked yet")


def main():
    """Main function to run the application"""
    root = Tk()
    app = PhoneTracker(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application closed by user")
    except Exception as e:
        print(f"Application error: {e}")


if __name__ == "__main__":
    main()