
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json

API_KEY = "__________________________________"

def format_person(person):
    lines = []
    fn = person.get("full_name") or (f'{person.get("first_name","")} {person.get("last_name","")}'.strip())
    if fn: lines.append(f"Name: {fn}")
    jt = person.get("job_title")
    if jt: lines.append(f"Title: {jt}")
    company = person.get("job_company_name")
    if company: lines.append(f"Employer: {company}")
    loc = person.get("location_name")
    if loc: lines.append(f"Location: {loc}")

    dob = person.get("birth_date") or person.get("date_of_birth")
    if dob: lines.append(f"Date of Birth: {dob}")

    age = person.get("age")
    if age: lines.append(f"Age: {age}")

    sex = person.get("sex") or person.get("gender")
    if sex: lines.append(f"Sex: {sex}")

    work_email = person.get("work_email")
    if work_email: lines.append(f"Work Email: {work_email}")

    personal_emails = person.get("personal_emails", [])
    if personal_emails: lines.append(f"Personal Emails: {', '.join(personal_emails)}")

    phones = person.get("phone_numbers", [])
    if phones: lines.append(f"Current Phones: {', '.join(phones)}")

    prev_phones = person.get("previous_phone_numbers", [])
    if prev_phones: lines.append(f"Previous Phones: {', '.join(prev_phones)}")

    addresses = person.get("street_addresses", [])
    if addresses:
        addr_lines = [a.get("display") for a in addresses if a.get("display")]
        lines.append(f"Addresses: {', '.join(addr_lines)}")

    prev_addresses = person.get("previous_addresses", [])
    if prev_addresses:
        addr_lines = [a.get("display") for a in prev_addresses if a.get("display")]
        lines.append(f"Previous Addresses: {', '.join(addr_lines)}")

    linkedin = person.get("linkedin_url")
    if linkedin: lines.append(f"LinkedIn: {linkedin}")
    github = person.get("github_url")
    if github: lines.append(f"GitHub: {github}")
    twitter = person.get("twitter_url")
    if twitter: lines.append(f"Twitter: {twitter}")
    facebook = person.get("facebook_url")
    if facebook: lines.append(f"Facebook: {facebook}")

    education = person.get("education", [])
    if education: lines.append(f"Education: {education}")

    work_history = person.get("work_experience", [])
    if work_history: lines.append(f"Work History: {work_history}")

    skills = person.get("skills", [])
    if skills: lines.append(f"Skills: {', '.join(skills)}")

    certifications = person.get("certifications", [])
    if certifications: lines.append(f"Certifications: {', '.join(certifications)}")

    return "\n".join(lines) + "\n" + ("-" * 48) + "\n"

def employee_lookup():
    company = emp_company_var.get().strip()
    city = emp_city_var.get().strip()
    state = emp_state_var.get().strip()
    first = emp_first_var.get().strip()
    last = emp_last_var.get().strip()
    industry = emp_industry_var.get().strip()
    domain = emp_domain_var.get().strip()
    linkedin = emp_linkedin_var.get().strip()
    size = emp_size_var.get().strip()
    sex = emp_sex_var.get().strip().lower()
    result_size = 30

    must = []
    if company:
        must.append({"match": {"job_company_name": company}})
    if city:
        must.append({"term": {"location_locality": city}})
    if state:
        must.append({"term": {"location_region": state}})
    if first:
        must.append({"term": {"first_name": first}})
    if last:
        must.append({"term": {"last_name": last}})
    if industry:
        must.append({"match": {"job_company_industry": industry}})
    if domain:
        must.append({"term": {"job_company_website": domain}})
    if linkedin:
        must.append({"term": {"job_company_linkedin_url": linkedin}})
    if size:
        must.append({"term": {"job_company_size": size}})
    if sex:
        must.append({"term": {"sex": sex}})

    if not must:
        messagebox.showerror("Input Error", "Enter at least one field!")
        return

    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    url = "https://api.peopledatalabs.com/v5/person/search"
    query = {
        "query": {
            "bool": {
                "must": must
            }
        },
        "size": result_size,
        "fields": ["*"]
    }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(query), timeout=25)
        result = r.json()
        emp_output.delete(1.0, tk.END)
        data = result.get("data", [])
        if not data:
            emp_output.insert(tk.END, "No employees found. Try a different search.")
            return
        for person in data:
            emp_output.insert(tk.END, format_person(person))
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

def person_lookup():
    first = lookup_first_var.get().strip()
    last = lookup_last_var.get().strip()
    city = lookup_city_var.get().strip()
    state = lookup_state_var.get().strip()
    size = 20

    must = []
    if first:
        must.append({"term": {"first_name": first}})
    if last:
        must.append({"term": {"last_name": last}})
    if city:
        must.append({"term": {"location_locality": city}})
    if state:
        must.append({"term": {"location_region": state}})

    if not must:
        messagebox.showerror("Input Error", "Enter at least one field!")
        return

    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    url = "https://api.peopledatalabs.com/v5/person/search"
    query = {
        "query": {
            "bool": {
                "must": must
            }
        },
        "size": size,
        "fields": ["*"]
    }
    try:
        r = requests.post(url, headers=headers, data=json.dumps(query), timeout=25)
        result = r.json()
        lookup_output.delete(1.0, tk.END)
        data = result.get("data", [])
        if not data:
            lookup_output.insert(tk.END, "No records found. Try a different search.")
            return
        for person in data:
            lookup_output.insert(tk.END, format_person(person))
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

def person_enrichment():
    email = enrich_email_var.get()
    first = enrich_first_var.get()
    last = enrich_last_var.get()
    phone = enrich_phone_var.get()
    linkedin = enrich_linkedin_var.get()
    city = enrich_city_var.get()
    state = enrich_state_var.get()
    params = {}
    if email: params["email"] = email
    if first: params["first_name"] = first
    if last: params["last_name"] = last
    if phone: params["phone"] = phone
    if linkedin: params["profile"] = linkedin
    if city: params["location_locality"] = city
    if state: params["location_region"] = state

    if not params:
        messagebox.showerror("Input Error", "Enter at least one field!")
        return

    headers = {"X-Api-Key": API_KEY}
    url = "https://api.peopledatalabs.com/v5/person/enrich"
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        result = r.json()
        enrich_output.delete(1.0, tk.END)
        if result.get("status") == 200 or result.get("data"):
            data = result.get("data", result)
            enrich_output.insert(tk.END, format_person(data))
        else:
            err = result.get("error", {}).get("message") or "No record found"
            enrich_output.insert(tk.END, err)
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

def lookup_company():
    domain = company_domain_var.get()
    linkedin = company_linkedin_var.get()
    name = company_name_var.get()
    params = {}
    if domain: params["website"] = domain
    if linkedin: params["profile"] = linkedin
    if name: params["name"] = name

    if not params:
        messagebox.showerror("Input Error", "Enter at least one field!")
        return

    headers = {"X-Api-Key": API_KEY}
    url = "https://api.peopledatalabs.com/v5/company/enrich"
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        result = r.json()
        company_output.delete(1.0, tk.END)
        if result.get("status") == 200 or result.get("name"):
            lines = []
            disp = result.get("display_name") or result.get("name")
            if disp: lines.append(f"Name: {disp}")
            web = result.get("website")
            if web: lines.append(f"Website: {web}")
            size = result.get("size")
            if size: lines.append(f"Size: {size}")
            founded = result.get("founded")
            if founded: lines.append(f"Founded: {founded}")
            industry = result.get("industry")
            if industry: lines.append(f"Industry: {industry}")
            hq = result.get("location", {}).get("name")
            if hq: lines.append(f"HQ: {hq}")
            linkedin = result.get("linkedin_url")
            if linkedin: lines.append(f"LinkedIn: {linkedin}")
            twitter = result.get("twitter_url")
            if twitter: lines.append(f"Twitter: {twitter}")
            facebook = result.get("facebook_url")
            if facebook: lines.append(f"Facebook: {facebook}")
            tags = result.get("tags")
            if tags: lines.append(f"Tags: {', '.join(tags)}")
            summary = result.get("summary")
            if summary: lines.append(f"Summary: {summary[:220]}{'...' if len(summary) > 220 else ''}")
            if not lines:
                company_output.insert(tk.END, "No data found (try a different input)")
            else:
                company_output.insert(tk.END, "\n".join(lines))
        else:
            err = result.get("error", {}).get("message") or "No record found"
            company_output.insert(tk.END, err)
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

root = tk.Tk()
root.title("PDL Lookup (PRO)")
root.geometry("1200x820")

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Employee Lookup by State')
tabControl.add(tab2, text='Person Lookup')
tabControl.add(tab3, text='Person Enrichment')
tabControl.add(tab4, text='Company Lookup')
tabControl.pack(expand=1, fill="both")

tk.Label(tab1, text="Company Name:").grid(row=0, column=0, sticky='w')
emp_company_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_company_var, width=26).grid(row=0, column=1, sticky='w')

tk.Label(tab1, text="Industry:").grid(row=0, column=2, sticky='w')
emp_industry_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_industry_var, width=20).grid(row=0, column=3, sticky='w')

tk.Label(tab1, text="Company Domain:").grid(row=1, column=2, sticky='w')
emp_domain_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_domain_var, width=20).grid(row=1, column=3, sticky='w')

tk.Label(tab1, text="Company LinkedIn:").grid(row=2, column=2, sticky='w')
emp_linkedin_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_linkedin_var, width=20).grid(row=2, column=3, sticky='w')

tk.Label(tab1, text="Company Size:").grid(row=3, column=2, sticky='w')
emp_size_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_size_var, width=20).grid(row=3, column=3, sticky='w')

tk.Label(tab1, text="Sex:").grid(row=4, column=2, sticky='w')
emp_sex_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_sex_var, width=20).grid(row=4, column=3, sticky='w')

tk.Label(tab1, text="City:").grid(row=1, column=0, sticky='w')
emp_city_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_city_var, width=26).grid(row=1, column=1, sticky='w')

tk.Label(tab1, text="State/Region:").grid(row=2, column=0, sticky='w')
emp_state_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_state_var, width=26).grid(row=2, column=1, sticky='w')

tk.Label(tab1, text="First Name:").grid(row=3, column=0, sticky='w')
emp_first_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_first_var, width=18).grid(row=3, column=1, sticky='w')

tk.Label(tab1, text="Last Name:").grid(row=4, column=0, sticky='w')
emp_last_var = tk.StringVar()
tk.Entry(tab1, textvariable=emp_last_var, width=18).grid(row=4, column=1, sticky='w')

tk.Button(tab1, text="Search", command=employee_lookup, bg="#456", fg="white").grid(row=5, column=0, columnspan=4, pady=12)
emp_output = scrolledtext.ScrolledText(tab1, wrap=tk.WORD, width=135, height=22, font=("Consolas", 11))
emp_output.grid(row=6, column=0, columnspan=4, padx=8, pady=8)

tk.Label(tab2, text="First Name:").grid(row=0, column=0, sticky='w')
lookup_first_var = tk.StringVar()
tk.Entry(tab2, textvariable=lookup_first_var, width=18).grid(row=0, column=1, sticky='w')

tk.Label(tab2, text="Last Name:").grid(row=1, column=0, sticky='w')
lookup_last_var = tk.StringVar()
tk.Entry(tab2, textvariable=lookup_last_var, width=18).grid(row=1, column=1, sticky='w')

tk.Label(tab2, text="City:").grid(row=2, column=0, sticky='w')
lookup_city_var = tk.StringVar()
tk.Entry(tab2, textvariable=lookup_city_var, width=26).grid(row=2, column=1, sticky='w')

tk.Label(tab2, text="State/Region:").grid(row=3, column=0, sticky='w')
lookup_state_var = tk.StringVar()
tk.Entry(tab2, textvariable=lookup_state_var, width=26).grid(row=3, column=1, sticky='w')

tk.Button(tab2, text="Search", command=person_lookup, bg="#456", fg="white").grid(row=4, column=0, columnspan=2, pady=12)
lookup_output = scrolledtext.ScrolledText(tab2, wrap=tk.WORD, width=135, height=22, font=("Consolas", 11))
lookup_output.grid(row=5, column=0, columnspan=2, padx=8, pady=8)

tk.Label(tab3, text="Email:").grid(row=0, column=0, sticky='w')
enrich_email_var = tk.StringVar()
tk.Entry(tab3, textvariable=enrich_email_var, width=32).grid(row=0, column=1, sticky='w')

tk.Label(tab3, text="First Name:").grid(row=1, column=0, sticky='w')
enrich_first_var = tk.StringVar()
tk.Entry(tab3, textvariable=enrich_first_var, width=18).grid(row=1, column=1, sticky='w')

tk.Label(tab3, text="Last Name:").grid(row=2, column=0, sticky='w')
enrich_last_var = tk.StringVar()
tk.Entry(tab3, textvariable=enrich_last_var, width=18).grid(row=2, column=1, sticky='w')

tk.Label(tab3, text="Phone:").grid(row=3, column=0, sticky='w')
enrich_phone_var = tk.StringVar()
tk.Entry(tab3, textvariable=enrich_phone_var, width=22).grid(row=3, column=1, sticky='w')

tk.Label(tab3, text="City:").grid(row=4, column=0, sticky='w')
enrich_city_var = tk.StringVar()
tk.Entry(tab3, textvariable=enrich_city_var, width=22).grid(row=4, column=1, sticky='w')

tk.Label(tab3, text="State/Region:").grid(row=5, column=0, sticky='w')
enrich_state_var = tk.StringVar()
tk.Entry(tab3, textvariable=enrich_state_var, width=22).grid(row=5, column=1, sticky='w')

tk.Label(tab3, text="LinkedIn URL:").grid(row=6, column=0, sticky='w')
enrich_linkedin_var = tk.StringVar()
tk.Entry(tab3, textvariable=enrich_linkedin_var, width=32).grid(row=6, column=1, sticky='w')

tk.Button(tab3, text="Search", command=person_enrichment, bg="#456", fg="white").grid(row=7, column=0, columnspan=2, pady=12)
enrich_output = scrolledtext.ScrolledText(tab3, wrap=tk.WORD, width=135, height=18, font=("Consolas", 11))
enrich_output.grid(row=8, column=0, columnspan=2, padx=8, pady=8)

tk.Label(tab4, text="Domain (website):").grid(row=0, column=0, sticky='w')
company_domain_var = tk.StringVar()
tk.Entry(tab4, textvariable=company_domain_var, width=30).grid(row=0, column=1, sticky='w')

tk.Label(tab4, text="LinkedIn URL:").grid(row=1, column=0, sticky='w')
company_linkedin_var = tk.StringVar()
tk.Entry(tab4, textvariable=company_linkedin_var, width=30).grid(row=1, column=1, sticky='w')

tk.Label(tab4, text="Company Name:").grid(row=2, column=0, sticky='w')
company_name_var = tk.StringVar()
tk.Entry(tab4, textvariable=company_name_var, width=30).grid(row=2, column=1, sticky='w')

tk.Button(tab4, text="Search", command=lookup_company, bg="#456", fg="white").grid(row=3, column=0, columnspan=2, pady=12)
company_output = scrolledtext.ScrolledText(tab4, wrap=tk.WORD, width=135, height=18, font=("Consolas", 11))
company_output.grid(row=4, column=0, columnspan=2, padx=8, pady=8)

root.mainloop()
