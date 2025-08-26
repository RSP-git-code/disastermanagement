from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dangerplot import generate_map
import risks_perlocation
from django.utils.safestring import mark_safe
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from google import genai
import json
import os
from risks_perlocation import analyze_country, country_aliases, df
from django.conf import settings
import google.generativeai as genai



def index(request):
    return render(request, "disasterpredictor/index.html")

@login_required
def dashboard(request):
    return render(request, "disasterpredictor/dashboard.html")

@login_required
def worldmap(request):
    chart_html = generate_map()
    return render(request, "disasterpredictor/worldmap.html", {"chart": chart_html})

countries_list = risks_perlocation.df["Location"].dropna().unique().tolist()

@login_required
def country_analysis(request):
    # Get all unique countries from the dataframe
    countries = sorted(df['Location'].dropna().unique())
    
    country = ''
    frequency_data = None
    chart = None
    table = None
    explanation = None
    error = None

    if request.method == 'POST':
        country = request.POST.get('country', '').strip()
        summary, fig = analyze_country(country)
        if summary is not None:
            frequency_data = summary.set_index('Disaster_Type').to_dict(orient='index')
            chart = fig.to_html(full_html=False)
            table = summary.to_html(classes="table table-striped")
        else:
            error = "No data available for this country."

    context = {
        'countries': countries,
        'country_aliases': country_aliases,
        'country': country,
        'frequency_data': frequency_data,
        'chart': chart,
        'table': table,
        'explanation': explanation,
        'error': error
    }

    return render(request, 'disasterpredictor/country.html', context)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # explicitly specify backend since multiple backends are active
            backend = "disasterpredictor.backends.EmailBackend"
            login(request, user, backend=backend)

            messages.success(request, f"🎉 Welcome, {user.email}!")
            return redirect("dashboard")
        else:
            messages.error(request, "❌ Please correct the errors below")
    else:
        form = CustomUserCreationForm()
    return render(request, "disasterpredictor/signup.html", {"form": form})
def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)  # username=email works with backend
        if user is not None:
            login(request, user)
            messages.success(request, f"👋 Welcome back, {user.email}!")
            return redirect("dashboard")
        else:
            messages.error(request, "❌ Invalid email or password")
    return render(request, "disasterpredictor/login.html")

def custom_logout(request):
    logout(request)
    messages.success(request, "✅ You have been logged out successfully.")
    return redirect("index")
# Initialize Gemini client
import sys
from google import genai
from google.genai import types

  # ✅ must include "models/"
from risks_perlocation import analyze_country
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
# Gemini setup
# GOOGLE_API_KEY =
# client = genai.Client(api_key=GOOGLE_API_KEY, http_options=types.HttpOptions(api_version="v1alpha"))
# generation_config = types.GenerateContentConfig(
#     temperature=0.7, top_p=0.95, top_k=20,
#     candidate_count=1, max_output_tokens=200
# )
from django.shortcuts import render
from risks_perlocation import analyze_country, df, country_aliases
from django.views.decorators.csrf import csrf_exempt

generation_config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=20,
    candidate_count=1,
    max_output_tokens=200
)
model_name = "models/gemini-2.0-flash-001"
def build_country_analysis(country):
    """
    Runs analyze_country() and prepares HTML for table + chart.
    Returns: table_html, chart_html, summary (DataFrame)
    """
    summary, fig = analyze_country(country)
    if summary is None or fig is None:
        return None, None, None  # ✅ return 3 values

    table_html = summary.to_html(classes="table table-bordered", index=False)
    chart_html = fig.to_html(full_html=False, include_plotlyjs=False)

    return table_html, chart_html, summary  # ✅ 3 values
client = genai.Client(api_key=settings.GOOGLE_API_KEY)
generation_config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=20,
    candidate_count=1,
    max_output_tokens=200
)
model_name = "models/gemini-2.0-flash-001"

@csrf_exempt
def explain_graph(request):
    explanation, country, table_html, chart_html = None, None, None, None
    countries = sorted(df["Location"].dropna().unique().tolist())

    if request.method == "POST":
        country = request.POST.get("country")
        action = request.POST.get("action")  # ✅ detect which button was pressed

        if action == "analyze":
            # Just show table + chart
            table_html, chart_html, summary = build_country_analysis(country)

        elif action == "explain":
            # Build summary, then call Gemini
            table_html, chart_html, summary = build_country_analysis(country)

            if summary is not None and not summary.empty:
                table_summary = "\n".join(
                    f"{row['Disaster_Type']}: Count={row['Count']}, "
                    f"Z-Score={row['z_score']:.2f}, Risk={row['Risk_Level']}"
                    for _, row in summary.iterrows()
                )

                prompt =f"""You are an expert disaster analyst.

Explain only what is z-score and the **pie chart** of disaster risk prediction for {country} in 4-5 short sentences.  
Do not explain tables, methods, or calculations.

The pie chart (already shown) displays the distribution of predicted disaster types based on past data.  
Summarize only the key insights:
- Which disaster types are most frequent  
- What their general risk level is (Danger, Low, or Safe)  

Keep it concise, simple, and easy to understand.  
Here is the data summary:
{table_summary}
{chart_html}
"""

                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt],
                    config=generation_config,
                )

                if response and response.candidates:
                    explanation = response.candidates[0].content.parts[0].text
                else:
                    explanation = "[No valid response]"

    return render(request, "disasterpredictor/country.html", {
        "country": country,
        "table": table_html,
        "chart": chart_html,
        "explanation": explanation,
        "countries": countries,
        "country_aliases": country_aliases,
    })




