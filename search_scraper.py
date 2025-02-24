import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import sys
import time
import json
from tkinter import PhotoImage
import pyperclip  # For clipboard functionality
from fpdf import FPDF
import os
import webbrowser

class BibleVerseFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Bible Verse Finder")
        self.root.geometry("800x600")
        
        # Center the main window
        self.center_window(self.root)
        
        # Initialize history and favorites
        self.search_history = []
        self.favorites = self.load_favorites()
        
        # Configure error handling
        self.root.report_callback_exception = self.show_error
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        self.create_menu()
        
        # Title Label
        self.title_label = ttk.Label(
            self.main_frame, 
            text="What Does the Bible Say About...", 
            font=('Arial', 16, 'bold')
        )
        self.title_label.pack(pady=(0, 20))
        
        # Create search frame
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Search Entry
        self.search_entry = ttk.Entry(self.search_frame, width=40, font=('Arial', 12))
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Button frame for alignment
        button_frame = ttk.Frame(self.search_frame)
        button_frame.pack(side=tk.LEFT)
        
        # Search Button
        self.search_button = ttk.Button(
            button_frame, 
            text="Find Bible Verses", 
            command=self.perform_search,
            style='Accent.TButton'
        )
        self.search_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Random Topic Button
        self.random_button = ttk.Button(
            button_frame,
            text="🎲 Random Topic",
            command=self.suggest_random_topic,
            style='Random.TButton'
        )
        self.random_button.pack(side=tk.LEFT)
        
        # Progress bar (hidden by default)
        self.progress = ttk.Progressbar(
            self.search_frame, 
            mode='indeterminate',
            length=200
        )
        self.progress.pack(side=tk.LEFT, padx=(10, 0))
        self.progress.pack_forget()
        
        # Results Area with right-click menu (read-only)
        self.results_area = scrolledtext.ScrolledText(
            self.main_frame, 
            wrap=tk.WORD, 
            height=25,
            font=('Arial', 11),
            state='disabled'  # Make it read-only
        )
        self.results_area.pack(fill=tk.BOTH, expand=True)
        
        # Create right-click menu
        self.create_context_menu()
        
        # Configure style for better appearance
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 11))
        
        # Bind Enter key to search
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        
        # Create a session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

        # Add after other initializations
        self.suggested_topics = {
            'Life Challenges': [
                'anxiety', 'stress', 'depression', 'fear', 'worry', 'anger',
                'loneliness', 'patience', 'peace', 'strength'
            ],
            'Relationships': [
                'love', 'marriage', 'family', 'friendship', 'forgiveness',
                'kindness', 'respect', 'trust', 'communication'
            ],
            'Faith & Growth': [
                'faith', 'prayer', 'wisdom', 'hope', 'guidance', 'purpose',
                'healing', 'gratitude', 'joy', 'perseverance'
            ],
            'Daily Living': [
                'work', 'money', 'success', 'decisions', 'leadership',
                'integrity', 'discipline', 'responsibility'
            ]
        }

        # Add donation button after search frame
        donation_frame = ttk.Frame(self.main_frame)
        donation_frame.pack(fill=tk.X, pady=(0, 10))
        
        donate_button = ttk.Button(
            donation_frame,
            text="❤ Support this Project",
            command=self.show_donation,
            style='Donation.TButton'
        )
        donate_button.pack(side=tk.RIGHT)
        
        # Configure donation button style
        style = ttk.Style()
        style.configure('Donation.TButton', 
                       font=('Arial', 10),
                       foreground='#d62828')

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Add Export submenu
        export_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Export", menu=export_menu)
        export_menu.add_command(label="Export Current Results to PDF", command=lambda: self.export_verses("current", "pdf"))
        export_menu.add_command(label="Export Current Results to TXT", command=lambda: self.export_verses("current", "txt"))
        export_menu.add_command(label="Export Favorites to PDF", command=lambda: self.export_verses("favorites", "pdf"))
        export_menu.add_command(label="Export Favorites to TXT", command=lambda: self.export_verses("favorites", "txt"))
        
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # History menu
        self.history_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="History", menu=self.history_menu)
        
        # Favorites menu
        self.favorites_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Favorites", menu=self.favorites_menu)
        self.update_favorites_menu()

        # Add Help/About menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Visit OpenBible.info", command=lambda: webbrowser.open("https://www.openbible.info"))

    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_selected)
        self.context_menu.add_command(label="Add Verse to Favorites", command=self.add_to_favorites)
        
        self.results_area.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        try:
            # Get the index where the user clicked
            click_index = self.results_area.index(f"@{event.x},{event.y}")
            
            # Find the verse at the clicked position
            start_index = "1.0"
            while True:
                # Find the next reference tag
                ref_start = self.results_area.tag_nextrange("reference", start_index)
                if not ref_start:
                    break
                    
                # Find the next verse text tag
                verse_start = self.results_area.tag_nextrange("verse_text", ref_start[1])
                if not verse_start:
                    break
                    
                # Find the next reference (or end of text)
                next_ref = self.results_area.tag_nextrange("reference", verse_start[1])
                verse_end = next_ref[0] if next_ref else "end"
                
                # Check if click is within this verse
                if self.results_area.compare(ref_start[0], "<=", click_index) and \
                   self.results_area.compare(verse_end, ">=", click_index):
                    # Select the entire verse
                    self.results_area.tag_remove("sel", "1.0", "end")
                    self.results_area.tag_add("sel", ref_start[0], verse_end)
                    break
                
                start_index = verse_end
            
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def copy_selected(self):
        try:
            selected_text = self.results_area.get("sel.first", "sel.last")
            pyperclip.copy(selected_text)
        except tk.TclError:
            messagebox.showinfo("Copy", "Please select text to copy")

    def add_to_favorites(self):
        try:
            # Get the selected text (which should be the entire verse)
            selected_text = self.results_area.get("sel.first", "sel.last")
            
            # Find the verse reference and text within the selection
            ref_start = self.results_area.tag_nextrange("reference", "sel.first", "sel.last")
            verse_start = self.results_area.tag_nextrange("verse_text", "sel.first", "sel.last")
            
            if ref_start and verse_start:
                # Get the verse reference and text
                verse_ref = self.results_area.get(ref_start[0], ref_start[1]).strip()
                verse_text = self.results_area.get(verse_start[0], verse_start[1]).strip()
                complete_verse = f"{verse_ref}\n{verse_text}"
                
                # Add to favorites if not already present
                if complete_verse not in self.favorites:
                    self.favorites.append(complete_verse)
                    self.save_favorites()
                    self.update_favorites_menu()
                    messagebox.showinfo("Favorites", f"Added to favorites:\n{verse_ref}")
                else:
                    messagebox.showinfo("Favorites", "This verse is already in your favorites!")
            else:
                messagebox.showinfo("Favorites", "Please right-click on a verse to add to favorites")
            
        except tk.TclError:
            messagebox.showinfo("Favorites", "Please right-click on a verse to add to favorites")

    def load_favorites(self):
        try:
            with open('favorites.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_favorites(self):
        with open('favorites.json', 'w') as f:
            json.dump(self.favorites, f)

    def update_favorites_menu(self):
        self.favorites_menu.delete(0, tk.END)
        
        if not self.favorites:
            self.favorites_menu.add_command(
                label="No favorites yet",
                state='disabled'
            )
            return
            
        for fav in self.favorites:
            # Create a submenu for each favorite
            fav_menu = tk.Menu(self.favorites_menu, tearoff=0)
            
            # Truncate long favorites for menu display
            menu_text = (fav[:50] + '...') if len(fav) > 50 else fav
            
            # Add the favorite verse submenu
            self.favorites_menu.add_cascade(
                label=menu_text,
                menu=fav_menu
            )
            
            # Add options to the submenu
            fav_menu.add_command(
                label="Show Verse",
                command=lambda f=fav: self.show_favorite(f)
            )
            fav_menu.add_command(
                label="Remove from Favorites",
                command=lambda f=fav: self.remove_favorite(f)
            )

    def remove_favorite(self, favorite):
        if favorite in self.favorites:
            self.favorites.remove(favorite)
            self.save_favorites()
            self.update_favorites_menu()
            
            # Get just the reference part for the message
            ref = favorite.split('\n')[0] if '\n' in favorite else favorite[:50]
            messagebox.showinfo("Favorites", f"Removed from favorites:\n{ref}")

    def show_favorite(self, favorite):
        # Enable temporarily to update text
        self.results_area.config(state='normal')
        self.results_area.delete(1.0, tk.END)
        
        # Split the favorite into reference and text
        lines = favorite.split('\n', 1)
        if len(lines) == 2:
            self.results_area.insert(tk.END, lines[0] + '\n', "reference")
            self.results_area.insert(tk.END, lines[1] + '\n', "verse_text")
        else:
            self.results_area.insert(tk.END, favorite)
            
        # Make read-only again
        self.results_area.config(state='disabled')

    def update_history(self, search_term):
        if search_term in self.search_history:
            self.search_history.remove(search_term)
        self.search_history.insert(0, search_term)
        self.search_history = self.search_history[:10]  # Keep only last 10 searches
        self.update_history_menu()

    def update_history_menu(self):
        self.history_menu.delete(0, tk.END)
        for term in self.search_history:
            self.history_menu.add_command(
                label=term,
                command=lambda t=term: self.search_from_history(t)
            )
        if not self.search_history:
            self.history_menu.add_command(
                label="No recent searches",
                state='disabled'
            )

    def search_from_history(self, term):
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, term)
        self.perform_search()

    def show_error(self, exc_type, exc_value, exc_traceback):
        error_message = f"An error occurred:\n{exc_type.__name__}: {exc_value}"
        messagebox.showerror("Error", error_message)

    def show_about(self):
        about_dialog = tk.Toplevel(self.root)
        about_dialog.title("About Bible Verse Finder")
        about_dialog.geometry("400x600")
        about_dialog.resizable(False, False)
        
        # Add padding frame
        main_frame = ttk.Frame(about_dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Program info
        ttk.Label(main_frame, 
                 text="Bible Verse Finder",
                 font=('Arial', 16, 'bold')).pack(pady=(0,10))
        
        # Version info and description
        ttk.Label(main_frame, 
                 text="Version 1.0\n\n" +
                      "Verse data provided by OpenBible.info\n" +
                      "Verses are from English Standard Version (ESV)",
                 justify=tk.CENTER).pack(pady=(0,20))
        
        # Donation section
        ttk.Label(main_frame,
                 text="Support this project",
                 font=('Arial', 12, 'bold')).pack(pady=(0,10))
        
        # Venmo button
        def open_venmo():
            # Replace with your Venmo username
            webbrowser.open("https://venmo.com/lilow")
        
        venmo_frame = ttk.Frame(main_frame)
        venmo_frame.pack(pady=(0,20))
        
        ttk.Button(venmo_frame,
                  text="Donate with Venmo",
                  command=open_venmo).pack(side=tk.LEFT, padx=5)
        
        # If you have a Venmo QR code image
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            qr_path = os.path.join(script_dir, "qr.png")
            
            if os.path.exists(qr_path):
                qr_image = PhotoImage(file=qr_path)
                qr_button = ttk.Label(main_frame, image=qr_image, cursor="hand2")
                qr_button.image = qr_image
                qr_button.pack(pady=(0,10))
                qr_button.bind("<Button-1>", lambda e: webbrowser.open("https://venmo.com/lilow"))
                
                ttk.Label(main_frame,
                         text="Click QR code or scan with your phone",
                         justify=tk.CENTER).pack()
        except Exception as e:
            print(f"Error loading QR code: {e}")
            ttk.Label(main_frame,
                     text="Error loading QR code",
                     justify=tk.CENTER).pack()
        
        # Close button
        ttk.Button(main_frame,
                  text="Close",
                  command=about_dialog.destroy).pack(pady=(10,0))
        
        # Center the dialog
        self.center_window(about_dialog)

    def perform_search(self):
        # Show progress bar
        self.progress.pack()
        self.progress.start(10)
        self.search_button.config(state='disabled')
        self.root.update_idletasks()

        try:
            # Enable temporarily to clear and update text
            self.results_area.config(state='normal')
            
            # Clear previous results
            self.results_area.delete(1.0, tk.END)
            
            search_term = self.search_entry.get().strip()
            
            if not search_term:
                messagebox.showwarning("Warning", "Please enter a topic to search for Bible verses.")
                return
            
            # Show searching message
            self.results_area.insert(tk.END, "Searching for Bible verses...\n\n")
            self.root.update_idletasks()
            
            # Update search history
            self.update_history(search_term)
            
            # Construct the URL
            base_url = "https://www.openbible.info/topics/"
            search_url = f"{base_url}{search_term.lower().replace(' ', '_')}"
            
            print(f"Searching URL: {search_url}")  # Debug print
            
            # Make the request
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Clear the "Searching..." message
            self.results_area.delete(1.0, tk.END)
            
            # Find all verse elements - look for divs that start with 'verse'
            verses = soup.find_all('div', class_=lambda x: x and x.startswith('verse'))
            print(f"Found {len(verses)} verses")  # Debug print
            
            if verses:
                # Add title only
                self.results_area.insert(tk.END, f"Bible Verses About {search_term.title()}\n", "title")
                self.results_area.insert(tk.END, "All verses from English Standard Version (ESV)\n\n", "note")
                
                # Process each verse
                for verse in verses:
                    try:
                        ref_elem = verse.find('a', class_='bibleref')
                        if ref_elem:
                            verse_ref = ref_elem.text.strip()
                            
                            # Get the verse text (it's in the p tag)
                            text_elem = verse.find('p')
                            if text_elem:
                                verse_text = text_elem.text.strip()
                                
                                # Format and display the verse
                                self.results_area.insert(tk.END, f"{verse_ref} (ESV)\n", "reference")
                                self.results_area.insert(tk.END, f"{verse_text}\n\n", "verse_text")
                                print(f"Added verse: {verse_ref}")  # Debug print
                    except Exception as e:
                        print(f"Error processing verse: {e}")  # Debug print
                        continue
            else:
                self.results_area.insert(tk.END, 
                    f"No verses found for '{search_term}'. Please try:\n"
                    "• Checking your spelling\n"
                    "• Using different words\n"
                    "• Trying a more general topic"
                )
            
            # Configure tags for styling
            self.results_area.tag_configure("title", font=('Arial', 14, 'bold'))
            self.results_area.tag_configure("note", font=('Arial', 10, 'italic'), foreground='#666666')
            self.results_area.tag_configure("reference", font=('Arial', 11, 'bold'))
            self.results_area.tag_configure("verse_text", font=('Arial', 11))
                
        except requests.RequestException as e:
            print(f"Request error: {e}")  # Debug print
            messagebox.showerror("Error", f"Error fetching verses: {str(e)}")
        except Exception as e:
            print(f"General error: {e}")  # Debug print
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            # Make read-only again and hide progress bar
            self.results_area.config(state='disabled')
            self.progress.stop()
            self.progress.pack_forget()
            self.search_button.config(state='normal')
            self.root.update_idletasks()

    def export_verses(self, source="current", format="pdf"):
        try:
            # Get verses based on source
            if source == "current":
                verses = self.get_current_verses()
                default_filename = "bible_verses"
            else:  # favorites
                verses = self.get_favorites_verses()
                default_filename = "favorite_verses"
            
            if not verses:
                messagebox.showwarning("Export", 
                    "No verses to export!" if source == "current" 
                    else "No favorites to export!")
                return
            
            # Get save location
            file_types = [("PDF files", "*.pdf")] if format == "pdf" else [("Text files", "*.txt")]
            filename = filedialog.asksaveasfilename(
                defaultextension=f".{format}",
                filetypes=file_types,
                initialfile=default_filename
            )
            
            if not filename:
                return
                
            if format == "pdf":
                self.export_to_pdf(verses, filename)
            else:
                self.export_to_txt(verses, filename)
                
            messagebox.showinfo("Export", f"Successfully exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Error during export: {str(e)}")

    def get_current_verses(self):
        verses = []
        start_index = "1.0"
        
        while True:
            # Find next reference
            ref_range = self.results_area.tag_nextrange("reference", start_index)
            if not ref_range:
                break
                
            # Find next verse text
            verse_range = self.results_area.tag_nextrange("verse_text", ref_range[1])
            if not verse_range:
                break
            
            # Get the text
            ref = self.results_area.get(ref_range[0], ref_range[1]).strip()
            verse = self.results_area.get(verse_range[0], verse_range[1]).strip()
            
            verses.append((ref, verse))
            start_index = verse_range[1]
        
        return verses

    def get_favorites_verses(self):
        verses = []
        for fav in self.favorites:
            parts = fav.split('\n', 1)
            if len(parts) == 2:
                verses.append((parts[0].strip(), parts[1].strip()))
        return verses

    def export_to_pdf(self, verses, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        
        # Add title
        title = "Bible Verses" if filename.endswith("bible_verses.pdf") else "Favorite Verses"
        pdf.cell(0, 10, title, ln=True, align='C')
        pdf.ln(10)
        
        # Add verses
        pdf.set_font("Arial", size=12)
        for ref, verse in verses:
            pdf.set_font("Arial", 'B', 12)  # Bold for reference
            pdf.multi_cell(0, 10, ref)
            pdf.set_font("Arial", size=12)  # Normal for verse
            pdf.multi_cell(0, 10, verse)
            pdf.ln(5)
        
        pdf.output(filename)

    def export_to_txt(self, verses, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            title = "Bible Verses" if filename.endswith("bible_verses.txt") else "Favorite Verses"
            f.write(f"{title}\n\n")
            
            for ref, verse in verses:
                f.write(f"{ref}\n{verse}\n\n")

    def suggest_random_topic(self):
        """Suggest a random topic from the categories"""
        import random
        # Get random category and topic
        category = random.choice(list(self.suggested_topics.keys()))
        topic = random.choice(self.suggested_topics[category])
        
        # Update search entry
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, topic)
        
        # Show tooltip with category
        messagebox.showinfo("Random Topic", f"Category: {category}\nTopic: {topic}")
        
        # Perform search
        self.perform_search()

    def show_donation(self):
        """Show donation options dialog"""
        donation_dialog = tk.Toplevel(self.root)
        donation_dialog.title("Support Bible Verse Finder")
        donation_dialog.geometry("400x600")
        donation_dialog.resizable(False, False)
        
        main_frame = ttk.Frame(donation_dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, 
                 text="Support this Project",
                 font=('Arial', 16, 'bold')).pack(pady=(0,10))
        
        ttk.Label(main_frame,
                 text="Your support helps maintain and improve\nthis Bible study tool.",
                 justify=tk.CENTER).pack(pady=(0,20))
        
        # QR Code Frame
        qr_frame = ttk.Frame(main_frame)
        qr_frame.pack(pady=(0,20))
        
        # Load and display QR code
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            qr_path = os.path.join(script_dir, "qr.png")
            
            if os.path.exists(qr_path):
                # Create clickable QR code
                qr_image = PhotoImage(file=qr_path)
                qr_button = ttk.Label(qr_frame, image=qr_image, cursor="hand2")
                qr_button.image = qr_image  # Keep reference
                qr_button.pack(pady=(0,10))
                qr_button.bind("<Button-1>", lambda e: webbrowser.open("https://venmo.com/lilow"))
                
                ttk.Label(qr_frame,
                         text="Click QR code or scan with your phone",
                         justify=tk.CENTER).pack()
            else:
                ttk.Label(qr_frame,
                         text="QR code not found",
                         justify=tk.CENTER).pack()
        except Exception as e:
            print(f"Error loading QR code: {e}")
            ttk.Label(qr_frame,
                     text="Error loading QR code",
                     justify=tk.CENTER).pack()
        
        # Regular Venmo button as backup
        ttk.Button(main_frame,
                  text="Open Venmo Website",
                  command=lambda: webbrowser.open("https://venmo.com/lilow")).pack(pady=(10,0))
        
        ttk.Button(main_frame,
                  text="Close",
                  command=donation_dialog.destroy).pack(pady=(20,0))
        
        # Center the dialog
        self.center_window(donation_dialog)

    def center_window(self, window):
        """Center any window on the screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"+{x}+{y}")

def main():
    try:
        root = tk.Tk()
        app = BibleVerseFinder(root)
        root.mainloop()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()