import json
import random
from datetime import datetime, timedelta

articles = []

# List of interesting temperatures and a generic range
specifics = [
    (-273.15, "Absolute Zero"),
    (-40, "Intersection of Celsius and Fahrenheit"),
    (0, "Freezing point of water"),
    (10, "Cool autumn day"),
    (20, "Room temperature"),
    (37, "Normal human body temperature"),
    (100, "Boiling point of water")
]

# Add more to reach > 100
temps_c = sorted(list(set(
    [x[0] for x in specifics] + 
    list(range(-30, 0, 5)) + 
    list(range(1, 100, 1)) + 
    list(range(105, 150, 5)) +
    list(range(150, 300, 25))
)))
temps_c = temps_c[:110]

def get_random_date():
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 7, 15)
    random_days = random.randrange((end_date - start_date).days)
    dt = start_date + timedelta(days=random_days)
    return dt.strftime('%B %d, %Y'), dt.strftime('%Y-%m-%d')

def get_category(c):
    if c < 0:
        return {"slug": "sub-zero", "name": "Sub-Zero"}
    elif c < 20:
        return {"slug": "cool-mild", "name": "Cool & Mild"}
    elif c < 40:
        return {"slug": "warm-hot", "name": "Warm & Hot"}
    else:
        return {"slug": "extreme-heat", "name": "Extreme Heat"}

widget_html = """
<div class="glowing-widget">
    <h3 style="margin-top: 0; margin-bottom: 1rem; color: var(--primary-color);">Interactive Temperature Converter</h3>
    <p style="margin-bottom: 1.5rem; font-size: 1.05rem;">Try converting another value in real-time:</p>
    <div style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
        <input type="number" id="celsiusInput" placeholder="Celsius" style="padding: 0.85rem 1rem; border-radius: var(--radius-md); border: 2px solid var(--border-color); width: 140px; font-size: 1.1rem; outline: none; transition: border-color 0.3s; background: var(--bg-color); color: var(--text-color);" onfocus="this.style.borderColor='var(--primary-color)'" onblur="this.style.borderColor='var(--border-color)'" oninput="document.getElementById('fahrenheitInput').value = ((this.value * 9/5) + 32).toFixed(2)">
        <span style="font-weight: 800; font-size: 1.2rem; color: var(--primary-color);">°C &nbsp; = &nbsp; </span>
        <input type="number" id="fahrenheitInput" placeholder="Fahrenheit" style="padding: 0.85rem 1rem; border-radius: var(--radius-md); border: 2px solid var(--border-color); width: 140px; font-size: 1.1rem; outline: none; transition: border-color 0.3s; background: var(--bg-color); color: var(--text-color);" onfocus="this.style.borderColor='var(--secondary-color)'" onblur="this.style.borderColor='var(--border-color)'" oninput="document.getElementById('celsiusInput').value = ((this.value - 32) * 5/9).toFixed(2)">
        <span style="font-weight: 800; font-size: 1.2rem; color: var(--secondary-color);">°F</span>
    </div>
</div>
"""

science_sections = [
    """<h2>The Science Behind the Temperature Scales</h2>
    <p>The history of temperature measurement is a fascinating journey through scientific discovery. The Fahrenheit scale, proposed by Daniel Gabriel Fahrenheit in 1724, was originally based on the freezing point of a specific brine mixture. Fahrenheit chose this mixture because it represented the lowest temperature he could reliably reproduce in a laboratory setting at the time. He then designated the freezing point of pure water as 32 degrees and the human body temperature around 96 degrees (later adjusted to 98.6°F).</p>
    <p>In contrast, the Celsius scale, developed by Swedish astronomer Anders Celsius in 1742, was designed with a more universally accessible framework in mind. Celsius based his scale entirely on the properties of pure water at sea level. He defined the freezing point of water as 0 degrees and the boiling point as 100 degrees, creating a centigrade scale divided into 100 equal intervals. This logical, decimal-based system made Celsius the standard for scientific research and eventually the preferred temperature scale for most of the world.</p>""",
    
    """<h2>Historical Context of Celsius and Fahrenheit</h2>
    <p>Understanding why we use two different temperature scales requires a brief look at 18th-century scientific history. Daniel Gabriel Fahrenheit invented the first reliable mercury thermometer in 1714. A decade later, he introduced his temperature scale, anchoring 0°F to the freezing temperature of a brine solution (a mixture of water, ice, and ammonium chloride). This provided a practical, low-end benchmark for weather reporting in cold European climates.</p>
    <p>Anders Celsius, an astronomer working in Sweden, sought a simpler, more reproducible metric. In 1742, he proposed a centigrade scale relying solely on the phase changes of water. By setting the freezing point at 0°C and the boiling point at 100°C (originally reversed, but later corrected by Carl Linnaeus), Celsius created a system that was easily standardizable anywhere on Earth. Today, while the United States predominantly retains the Fahrenheit system for everyday use, the Celsius scale is universally employed in scientific disciplines and by the vast majority of nations globally.</p>""",
    
    """<h2>How the Temperature Scales Evolved</h2>
    <p>The conversion between Celsius and Fahrenheit is necessary today largely due to differing historical adoptions of scientific standards. The Fahrenheit scale was widely adopted across the British Empire throughout the 18th and 19th centuries. Its finer granularity—having 180 degrees between the freezing and boiling points of water compared to Celsius's 100 degrees—made it highly favored for precise meteorological tracking without needing to use fractions or decimals.</p>
    <p>However, the global shift towards the metric system in the mid-20th century saw most countries abandon Fahrenheit in favor of Celsius. The Celsius scale's simple 0-to-100 framework perfectly complemented the base-10 logic of the metric system. The multiplier of 1.8 (or 9/5) in our conversion formula exists precisely because an increment of 1 degree Celsius represents a larger change in thermal energy than 1 degree Fahrenheit. The offset of 32 degrees aligns the two distinct starting points for the freezing of water.</p>"""
]

for c in temps_c:
    f = round((c * 9/5) + 32, 2)
    
    # 1. Expand Range Context Paragraph
    if c == -273.15:
        context_p = "This specific measurement represents absolute zero. In thermodynamics, absolute zero is universally recognized as the theoretical lowest possible temperature. At this exact point, fundamental molecular motion ceases completely, and a thermodynamic system possesses its lowest possible energy. Scientists use specialized equipment like cryocoolers and laser cooling techniques to reach temperatures mere fractions of a degree above this point, allowing them to study bizarre quantum phenomena like Bose-Einstein condensates and superconductivity."
        is_hot = "Neither. It is the absolute coldest temperature physically possible in the universe."
    elif c == -40:
        context_p = "Interestingly, -40 is a unique and famous temperature because it is the exact point where the Celsius and Fahrenheit scales align seamlessly. Whether you are using a Celsius thermometer or a Fahrenheit thermometer, the reading is exactly -40. This temperature represents extreme, life-threatening cold. In environments that reach -40, exposed human skin can suffer from severe frostbite in a matter of minutes, and machinery often requires specialized heating elements just to function."
        is_hot = "Extremely cold. This is a life-threatening temperature requiring heavy arctic survival gear."
    elif c == 0:
        context_p = "0°C is widely recognized worldwide as the official freezing point of pure water at standard atmospheric pressure. This makes it one of the most critical benchmark temperatures in meteorology, geography, and daily life. When the ambient temperature drops to 0°C, precipitation transforms into snow or freezing rain, profoundly impacting transportation, infrastructure, and agriculture. It is the dividing line between liquid water and solid ice."
        is_hot = "Cold. It is the exact freezing point of water."
    elif c == 37:
        context_p = "37°C is generally acknowledged by medical professionals globally as the normal resting body temperature of a healthy human adult. The human body tightly regulates its internal temperature around this mark to ensure optimal enzyme function and metabolic stability. A sustained internal temperature reading significantly above 37°C indicates a fever and potential illness, while a reading significantly below indicates hypothermia."
        is_hot = "Warm. It matches the internal resting temperature of a healthy human body."
    elif c == 100:
        context_p = "100°C is definitively the boiling point of pure water at sea level under standard atmospheric conditions. This is the temperature at which liquid water rapidly vaporizes into steam. In culinary applications, bringing water to 100°C is essential for boiling pasta, sterilizing equipment, and preparing hot beverages like tea and coffee. In industrial settings, steam generated at and above this temperature drives turbines that produce a massive percentage of the world's electricity."
        is_hot = "Extremely hot. It is the boiling point of water and will cause severe scalds instantly."
    elif c < 0:
        context_p = f"At {c}°C, ambient conditions are officially freezing and distinctly sub-zero. This harsh temperature is commonly encountered during deep winter months in northern latitudes, high-altitude mountain ranges, or within specialized commercial refrigeration and blast-freezing environments. Prolonged exposure to {c}°C without adequate thermal protection can rapidly lead to hypothermia and frostbite. When venturing into environments this cold, layered insulated clothing, heavy coats, and wind-blocking materials are absolutely essential."
        is_hot = "Very cold. It is well below the freezing point of water."
    elif 0 < c < 15:
        context_p = f"A temperature reading of {c}°C generally feels quite chilly. This is highly typical of early spring or late autumn weather patterns in temperate climate zones. While it is above freezing, the air retains a sharp crispness. When heading outside in {c}°C weather, most people will comfortably require a medium-weight jacket, a sweater, or long sleeves to stay warm. It is excellent weather for brisk outdoor activities like hiking or running, as the cooler air prevents rapid overheating."
        is_hot = "Cool to cold, depending on wind and humidity. A jacket is usually required outside."
    elif 15 <= c < 25:
        context_p = f"{c}°C is widely considered a mild, highly comfortable room temperature. This range is optimal for indoor living, office environments, and casual outdoor recreation without requiring extreme heating or heavy air conditioning mechanisms. In fact, many modern smart thermostats are programmed to maintain ambient indoor temperatures very close to this range to balance human comfort with energy efficiency. Clothing choices for {c}°C are highly versatile, ranging from t-shirts and jeans to light cardigans."
        is_hot = "Comfortable and mild. It is an ideal room temperature."
    elif 25 <= c < 35:
        context_p = f"At {c}°C, the surrounding weather is notably warm to hot. This is very typical of peak summer days in temperate regions, or year-round conditions in tropical and subtropical climates. When the temperature reaches {c}°C, air conditioning or heavy fan usage becomes common in households and commercial buildings. Outdoor activities should be accompanied by adequate hydration and sun protection, as prolonged exposure can lead to mild heat exhaustion."
        is_hot = "Warm to hot. It feels like a standard summer day."
    elif 35 <= c < 50:
        context_p = f"Reaching {c}°C indicates extremely hot, potentially hazardous conditions. Temperatures in this range are typically found in desert climates during peak summer or during severe, anomalous heatwaves in other regions. It can actually be dangerous for prolonged human exposure unless adequate hydration, shade, and air conditioning are strictly maintained. At {c}°C, the risk of heatstroke rises exponentially, and strenuous outdoor physical labor is strongly discouraged by health authorities."
        is_hot = "Dangerously hot. Prolonged outdoor exposure carries a high risk of heat illness."
    else:
        context_p = f"A high temperature of {c}°C is extremely intense. You will not encounter this naturally in Earth's atmosphere. Instead, it is typically associated with heavy industrial processes, commercial baking and cooking environments, or internal engine operating conditions. Managing temperatures of {c}°C requires specialized heat-resistant materials, strict safety protocols, and advanced thermal engineering to prevent structural damage or fires."
        is_hot = "Incredibly hot. It is an industrial or cooking temperature, far beyond human survival limits."

    # 2. Dynamic "Nearby Temperatures" Conversion Table
    table_rows = ""
    for offset in range(-5, 6):
        nearby_c = c + offset
        nearby_f = round((nearby_c * 9/5) + 32, 2)
        if offset == 0:
            table_rows += f"<tr style='background-color: var(--primary-color); color: white;'><td style='padding: 10px; border: 1px solid var(--border-color);'><strong>{nearby_c}°C</strong></td><td style='padding: 10px; border: 1px solid var(--border-color);'><strong>{nearby_f}°F</strong></td></tr>"
        else:
            table_rows += f"<tr><td style='padding: 10px; border: 1px solid var(--border-color);'>{nearby_c}°C</td><td style='padding: 10px; border: 1px solid var(--border-color);'>{nearby_f}°F</td></tr>"
            
    nearby_table = f"""
    <h2>Nearby Temperature Conversions</h2>
    <p>For your convenience, here is a quick reference table showing conversions for temperatures immediately surrounding {c}°C. This can be particularly useful for identifying trends or making quick mental approximations.</p>
    <table style="width: 100%; max-width: 400px; border-collapse: collapse; text-align: center; margin-bottom: 2rem; border: 1px solid var(--border-color);">
        <thead>
            <tr style="background-color: rgba(0,0,0,0.05);">
                <th style="padding: 10px; border: 1px solid var(--border-color);">Celsius (°C)</th>
                <th style="padding: 10px; border: 1px solid var(--border-color);">Fahrenheit (°F)</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    """

    # 3. Auto-Generated FAQ Section
    faqs = [
        {
            "q": f"Is {c} Celsius hot or cold?",
            "a": is_hot
        },
        {
            "q": f"How do I convert {c} Celsius to Fahrenheit without a calculator?",
            "a": f"A quick mental math trick to approximate the conversion is to multiply {c} by 2, and then add 30. While this won't give you the exact answer of {f}°F, it will get you very close for everyday estimations."
        },
        {
            "q": f"What is the exact mathematical formula to get {f}°F?",
            "a": f"The exact, universally accepted scientific formula is F = (C × 1.8) + 32. If you plug in {c} for C, the equation becomes ({c} × 1.8) + 32, which precisely equals {f}."
        }
    ]
    
    faq_html = "<h2>Frequently Asked Questions</h2><div class='faq-section'>"
    for faq in faqs:
        faq_html += f"<div style='margin-bottom: 1.5rem;'><strong>Q: {faq['q']}</strong><p style='margin-top: 0.5rem; color: #475569;'>A: {faq['a']}</p></div>"
    faq_html += "</div>"
    
    # Generate JSON-LD for FAQs
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    for faq in faqs:
        faq_schema["mainEntity"].append({
            "@type": "Question",
            "name": faq["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["a"]
            }
        })
    faq_schema_str = f'<script type="application/ld+json">\n{json.dumps(faq_schema, indent=2)}\n</script>'

    phrasings_p1 = [
        f"Converting temperatures from Celsius to Fahrenheit is a common requirement in many scientific, culinary, and everyday contexts. If you are starting with a measurement of <strong>{c}°C</strong>, it is highly beneficial to know exactly what that represents in the Fahrenheit system.",
        f"Whether you are closely following a foreign baking recipe, tracking global weather changes, or conducting a controlled science experiment, knowing how to accurately convert <strong>{c} degrees Celsius</strong> into Fahrenheit is essential. Here is the exact calculation.",
        f"Many people look for a reliable, fast way to translate <strong>{c}°C</strong> into the Fahrenheit scale. We have done the comprehensive math for you below to save you time and provide a precise, scientifically accurate measurement."
    ]

    phrasings_h2 = [
        f"How to Convert {c} Celsius to Fahrenheit",
        f"The Exact Calculation for {c}°C to °F",
        f"Step-by-Step Conversion for {c} Celsius"
    ]
    
    references = [
        """<div class="references" style="margin-top: 3rem; font-size: 0.95rem; color: #475569;">
            <h3>Authoritative References</h3>
            <ul>
                <li><a href="https://www.nist.gov/pml/weights-and-measures/si-units-temperature" target="_blank" rel="noopener noreferrer">NIST: SI Units &ndash; Temperature</a> - Official definitions of temperature scales.</li>
                <li><a href="https://www.weather.gov/wrn/winter_safety" target="_blank" rel="noopener noreferrer">Weather.gov: Temperature & Safety</a> - Guidelines on environmental temperatures.</li>
            </ul>
        </div>""",
        """<div class="references" style="margin-top: 3rem; font-size: 0.95rem; color: #475569;">
            <h3>Authoritative References</h3>
            <ul>
                <li><a href="https://www.nasa.gov/audience/forstudents/postsecondary/features/F_Temperature_and_Heat.html" target="_blank" rel="noopener noreferrer">NASA: Temperature and Heat</a> - Educational overview of thermodynamics.</li>
                <li><a href="https://www.noaa.gov/education/resource-collections/climate" target="_blank" rel="noopener noreferrer">NOAA Climate Resources</a> - Comprehensive climate data and temperature monitoring.</li>
            </ul>
        </div>"""
    ]

    date_display, date_iso = get_random_date()
    
    body_text = f"""
    {faq_schema_str}
    <p>{random.choice(phrasings_p1)}</p>
    
    <h2>{random.choice(phrasings_h2)}</h2>
    <p>The standard formula to convert Celsius to Fahrenheit is formally defined as: <code>F = (C × 9/5) + 32</code>. This can also be written as <code>F = (C × 1.8) + 32</code>.</p>
    <p>By substituting <strong>{c}</strong> directly into our formula, we can calculate the precise answer:</p>
    <ul>
      <li>First, multiply {c} by 1.8, which gives us a subtotal of {round(c * 1.8, 2)}.</li>
      <li>Next, add 32 to {round(c * 1.8, 2)} to yield the final, exact result of <strong>{f}°F</strong>.</li>
    </ul>
    
    {widget_html}

    <h2>Context and Practical Application for {c}°C</h2>
    <p>{context_p}</p>
    
    {nearby_table}
    
    {random.choice(science_sections)}
    
    {faq_html}
    
    <h3>Key Takeaways for this Calculation</h3>
    <div class="key-takeaways">
      <ul>
        <li><strong>Original Temperature Value:</strong> {c}°C</li>
        <li><strong>Fahrenheit Equivalent Value:</strong> {f}°F</li>
        <li><strong>Step-by-Step Calculation:</strong> ({c} × 1.8) + 32 = {f}</li>
      </ul>
    </div>

    {random.choice(references)}
    """

    articles.append({
        "title": f"{c} Celsius to Fahrenheit Conversion",
        "slug": f"convert-{c}-celsius-to-fahrenheit".replace('.', '-').replace('--', '-'),
        "category": get_category(c),
        "c": c,
        "f": f,
        "body": body_text,
        "description": f"Learn how to quickly and accurately convert {c} degrees Celsius to Fahrenheit with our fast calculator. The exact answer is {f}°F.",
        "date_display": date_display,
        "date_iso": date_iso,
        "author": "Editorial Team" if random.random() > 0.5 else "Sarah Metric, Technical Editor"
    })

with open('e:/Adsense sites/11-20/15/_src/_data/articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent=4)
print("Generated", len(articles), "articles.")
