import os

KB = "data/knowledge_base"
os.makedirs(KB, exist_ok=True)

docs = {}

# ---------------- PRODUCT CATALOG (10 docs) ----------------
docs["product_ceylon_cinnamon.md"] = """# Product: Ceylon True Cinnamon (Cinnamomum verum)
SKU: SST-CIN-001
Category: Spices
Origin: Matale & Kegalle districts, Sri Lanka
Grades available: Alba, C5 Special, C4, C5, M4, M5
Packaging: 25kg kraft bags (bulk), 250g/500g retail pouches
Minimum Order Quantity (MOQ): 500kg for bulk grades, 100 units for retail packs
Lead time: 15-20 working days from order confirmation
Current stock level: 4,200 kg (bulk, all grades combined)
Shelf life: 24 months from packing date if stored below 25C and away from moisture
Notes: True Ceylon cinnamon (not cassia). Quills are hand-rolled. Certificate of origin available on request.
"""

docs["product_black_pepper.md"] = """# Product: Ceylon Black Pepper (Piper nigrum)
SKU: SST-PEP-010
Category: Spices
Origin: Matale, Kandy, Kurunegala districts
Grades: MG1 (bold), FAQ, Special Extra Bold
Packaging: 50kg PP bags (bulk), 100g/200g retail jars
MOQ: 1,000kg bulk, 200 units retail
Lead time: 10-15 working days
Current stock level: 6,800 kg
Shelf life: 36 months, whole peppercorns
Notes: Steam-sterilised on request for EU/US import compliance. Piperine content typically 5-6%.
"""

docs["product_cloves.md"] = """# Product: Cloves (Syzygium aromaticum)
SKU: SST-CLV-014
Category: Spices
Origin: Matale district, Sri Lanka (secondary sourcing from Zanzibar partners for overflow orders)
Grades: Hand-picked whole cloves, clove stems (lower grade, for oil extraction)
Packaging: 25kg bags (bulk), 100g retail pouches
MOQ: 250kg bulk
Lead time: 12-18 working days
Current stock level: 1,150 kg
Shelf life: 24 months
Notes: Essential oil content minimum 15%. Suitable for both culinary and clove oil distillation buyers.
"""

docs["product_cardamom.md"] = """# Product: Green Cardamom (Elettaria cardamomum)
SKU: SST-CAR-022
Category: Spices
Origin: Central highlands, Nuwara Eliya region
Grades: 8mm Bold, 7mm, Mixed
Packaging: 10kg vacuum-sealed bags, 50g/100g retail tins
MOQ: 100kg bulk, 100 units retail
Lead time: 20-25 working days (limited seasonal harvest, Oct-Feb peak)
Current stock level: 310 kg (low - seasonal item)
Shelf life: 18 months if vacuum sealed, 12 months in standard packaging
Notes: One of the highest-value spice lines. Stock is seasonal; recommend pre-orders outside Oct-Feb window.
"""

docs["product_nutmeg_mace.md"] = """# Product: Nutmeg & Mace
SKU: SST-NUT-030 (nutmeg), SST-MAC-031 (mace)
Category: Spices
Origin: Matale, Kandy districts
Packaging: 25kg bags (nutmeg, bulk), 5kg bags (mace, bulk), 100g retail
MOQ: 200kg nutmeg, 50kg mace
Lead time: 15 working days
Current stock level: Nutmeg 900kg, Mace 140kg
Shelf life: 24 months
Notes: Mace is significantly higher value per kg than nutmeg and is often sold separately during processing.
"""

docs["product_ceylon_black_tea.md"] = """# Product: Ceylon Black Tea (Orthodox)
SKU: SST-TEA-040
Category: Tea
Origin: Nuwara Eliya (high-grown), Uva, Dimbula regions
Grades: OP (Orange Pekoe), BOP (Broken Orange Pekoe), FBOP, Dust (for tea bags)
Packaging: 22.5kg wooden tea chests (traditional export), 20kg multi-wall paper sacks, retail 100g/200g boxes
MOQ: 1 tea chest (22.5kg) bulk, 500 units retail boxes
Lead time: 10 working days (tea is processed weekly at partner factories)
Current stock level: 3,600 kg across grades
Shelf life: 24 months if kept dry and away from strong odours
Notes: High-grown Nuwara Eliya tea commands premium pricing. Single-estate lots available for specialty buyers.
"""

docs["product_ceylon_green_tea.md"] = """# Product: Ceylon Green Tea
SKU: SST-TEA-045
Category: Tea
Origin: Uva and Ratnapura regions
Grades: Sencha-style, Gunpowder-style
Packaging: 20kg sacks (bulk), 100g retail boxes
MOQ: 300kg bulk
Lead time: 12 working days
Current stock level: 520 kg
Shelf life: 18 months
Notes: Lower production volume than black tea; suitable for boutique buyers rather than large-volume retail chains.
"""

docs["product_vanilla.md"] = """# Product: Vanilla Beans (Vanilla planifolia)
SKU: SST-VAN-050
Category: Specialty
Origin: Matale (small-scale cultivation, limited supply)
Grades: Gourmet (Grade A), Extraction Grade (Grade B)
Packaging: Vacuum-sealed 1kg bundles
MOQ: 10kg
Lead time: 30-40 working days (very limited domestic production)
Current stock level: 45 kg (very low)
Shelf life: 12 months refrigerated
Notes: Highest-value product per kg. Supply is constrained; large orders (>25kg) should be pre-booked at least one harvest season ahead.
"""

docs["product_turmeric.md"] = """# Product: Turmeric (Curcuma longa)
SKU: SST-TUR-055
Category: Spices
Origin: Rajanganaya, Anuradhapura region
Form: Whole dried fingers, or ground powder (curcumin content 3-5%)
Packaging: 25kg bags (bulk), 250g retail pouches
MOQ: 500kg bulk
Lead time: 10 working days
Current stock level: 5,400 kg
Shelf life: 24 months whole, 12 months ground
Notes: High-volume, lower-margin product. Frequently ordered alongside pepper and cinnamon in mixed containers.
"""

docs["product_coconut_products.md"] = """# Product: Coconut-based Products
SKU: SST-COC-060 (desiccated coconut), SST-COC-061 (coconut oil, virgin)
Category: Coconut
Origin: Kurunegala, Puttalam coconut triangle
Packaging: 25kg bags (desiccated coconut), 20L jerry cans / 200L drums (virgin coconut oil)
MOQ: 500kg desiccated coconut, 200L oil
Lead time: 15 working days
Current stock level: Desiccated coconut 2,100 kg; VCO 1,800 L
Shelf life: Desiccated coconut 12 months; VCO 24 months
Notes: VCO is cold-pressed, certified organic on selected batches (batch certificates available).
"""

# ---------------- POLICIES (10 docs) ----------------
docs["policy_shipping.md"] = """# Shipping & Logistics Policy
All export shipments are handled FOB Colombo unless CIF or DDP terms are contractually agreed.
Standard sea freight lead time to major ports:
- EU (Rotterdam/Hamburg): 24-30 days
- USA (East Coast): 30-38 days
- Middle East (Dubai/Jebel Ali): 8-12 days
- Australia: 18-24 days
Air freight is available for orders under 500kg or urgent samples, at a surcharge of approximately 4-6x sea freight cost.
Consolidation: orders under 1 full container (20ft/40ft) may be consolidated with other shipments, adding 5-10 days to lead time.
All shipments include a packing list, commercial invoice, and certificate of origin. Phytosanitary certificates are issued per shipment at no extra cost for spice and tea exports.
"""

docs["policy_payment_terms.md"] = """# Payment Terms Policy
Standard terms for new buyers: 30% advance payment on order confirmation, 70% balance against copy of Bill of Lading (CAD - cash against documents).
Established buyers (3+ completed orders): Letter of Credit (LC at sight) or open account with 30-day terms may be negotiated.
Accepted payment methods: Telegraphic Transfer (T/T), Letter of Credit, and for orders under USD 2,000, PayPal is accepted with a 3.5% processing surcharge.
Currency: All quotations are in USD unless otherwise agreed. Prices are valid for 30 days from quotation date due to raw material price volatility, especially for cardamom and vanilla.
Late payment: Balances outstanding more than 15 days past the agreed due date accrue 1.5% monthly interest and may result in hold on future shipments.
"""

docs["policy_returns_refunds.md"] = """# Returns, Refunds & Claims Policy
Quality claims must be submitted within 14 days of container arrival at destination port, accompanied by an independent inspection report (e.g. SGS, Bureau Veritas, or equivalent) and photographic evidence.
Approved claims are resolved via one of: replacement in the next shipment, credit note against future orders, or partial refund proportional to the affected quantity - buyer's choice where feasible.
Claims related to moisture damage during ocean transit are handled case-by-case in coordination with the buyer's marine cargo insurance, as this typically falls outside seller liability once FOB terms are met.
No returns are accepted for custom-blended or private-label packaging orders once production has started, except in cases of proven quality defect.
Refunds, where approved, are processed within 21 business days via the original payment method.
"""

docs["policy_quality_certification.md"] = """# Quality Assurance & Certification
All products undergo in-house quality control including moisture content testing, foreign matter screening, and microbiological testing on sample batches.
Certifications held: ISO 22000 (Food Safety Management), HACCP, and Sri Lanka Export Development Board (EDB) registration.
Organic certification (EU Organic / USDA Organic equivalent) is available on selected product lines - currently virgin coconut oil and select cinnamon lots. Buyers requiring organic certification should specify at time of enquiry, as organic and conventional stock are kept separately.
Fumigation: Available on request for markets requiring methyl bromide or phosphine fumigation certificates (common for EU and Australian imports).
Third-party pre-shipment inspection can be arranged at buyer's cost through SGS or Intertek.
"""

docs["policy_export_documentation.md"] = """# Export Documentation Requirements
Standard document set provided with every shipment:
1. Commercial Invoice
2. Packing List
3. Bill of Lading (or Airway Bill for air shipments)
4. Certificate of Origin (issued via Ceylon Chamber of Commerce)
5. Phytosanitary Certificate (Department of Agriculture, Sri Lanka)
6. Fumigation Certificate (where applicable)
Additional documents available on request and may incur processing fees:
- GSP Form A (for preferential tariff markets)
- Halal Certification (available for spice lines, processed through SLHCC accredited certifier - allow 5 extra working days)
- Kosher Certification (available on select lines, allow 10 extra working days)
Buyers importing into the EU should note new EUDR (EU Deforestation Regulation) due diligence documentation is being phased in for relevant categories; contact us for current compliance status per product line.
"""

docs["policy_moq.md"] = """# Minimum Order Quantities (MOQ) Policy
MOQs vary by product and are listed on individual product sheets. General guidance:
- High-volume spices (pepper, turmeric, cinnamon): 250-1,000kg MOQ
- Low-volume/seasonal items (cardamom, vanilla): 10-100kg MOQ
- Tea: 1 chest (22.5kg) minimum, though container-load orders (typically 8-10 tonnes) receive preferential pricing
Mixed-container orders combining multiple products are accepted provided the combined order value exceeds USD 3,000.
Sample orders (under MOQ) are available for new buyers at a 20% price premium to cover handling costs, capped at 5kg per product per buyer per year.
"""

docs["policy_packaging_standards.md"] = """# Packaging Standards
Bulk export packaging default: multi-wall kraft paper bags with polyethylene liner, net weights as specified per product sheet.
Private label / custom packaging: available for orders exceeding 1,000kg per SKU, with a design and setup lead time of 3-4 weeks and a one-time plate/design charge (waived for orders over 5,000kg).
Palletisation: standard export pallets are 1.1m x 1.1m (Asia-Pacific standard); Euro-pallets (1.2m x 0.8m) available on request for EU-bound shipments at a small surcharge due to lower fill efficiency.
All packaging materials used are food-grade and compliant with FDA and EU food contact material regulations.
"""

docs["policy_storage_handling.md"] = """# Storage & Handling Guidelines
Warehouse conditions are maintained at ambient temperature with dehumidification, targeting relative humidity below 65% to prevent mould and moisture-related quality issues, particularly for cinnamon, cloves, and tea.
Pest control: warehouse is fumigated on a scheduled quarterly basis; stock rotation follows FIFO (first-in, first-out) based on production batch dates.
Buyers are advised to store received goods in cool, dry conditions away from direct sunlight and strong-odour substances, as spices and tea readily absorb ambient odours.
Maximum recommended re-storage period after receipt before repackaging into smaller retail units is 6 months to preserve optimal flavour and aroma.
"""

docs["policy_sustainability.md"] = """# Sustainability & Ethical Sourcing Practices
Sourcing is conducted through a network of small-holder farmer cooperatives across the identified growing regions, with direct-trade relationships covering approximately 60% of raw material volume as of the latest internal review.
Fair pricing commitments: farmer-gate prices are reviewed quarterly against Sri Lanka Export Development Board benchmark pricing to ensure farmers receive a fair share of export value.
Environmental practices: encouraging shade-grown cultivation for cardamom and pepper, and supporting reforestation initiatives in partnership with local agricultural extension offices.
Buyers interested in Fairtrade or Rainforest Alliance certified lines should enquire specifically, as certified volumes are limited and allocated on a first-confirmed basis each season.
"""

docs["policy_complaint_handling.md"] = """# Complaint Handling Procedure
Step 1: Buyer submits complaint via email to the assigned account contact, including order reference number, description of issue, and supporting evidence (photos, lab reports where relevant).
Step 2: Internal review is completed within 3 business days, including cross-check against retained reference samples from the same production batch.
Step 3: Resolution is proposed (replacement, credit, refund, or explanation where the claim is not substantiated) within 7 business days of complaint receipt.
Step 4: Escalation - if the buyer disputes the resolution, the matter is escalated to the Export Manager for final review. Unresolved disputes may be referred to mediation through the Ceylon Chamber of Commerce.
All complaints and resolutions are logged for quality trend analysis; recurring issues on a specific product line trigger a supplier-side quality audit.
"""

# ---------------- FAQ (3 docs) ----------------
docs["faq_general.md"] = """# General FAQ
Q: What is the minimum order value to start working with Serendib Spice & Tea Traders?
A: There is no fixed minimum order value, but MOQs apply per product (see MOQ policy). Sample orders are available for new buyers.

Q: Can you provide product samples before I place a bulk order?
A: Yes, samples up to 500g per product are provided free of charge (buyer pays courier cost); larger samples are charged at the sample pricing tier.

Q: Do you offer private label / white label packaging?
A: Yes, for orders exceeding 1,000kg per SKU. See Packaging Standards policy for lead times and costs.

Q: How do I get a formal quotation?
A: Send an enquiry with product, grade, quantity, and destination port; quotations are typically issued within 2 business days and are valid for 30 days.

Q: Is Serendib Spice & Tea Traders EDB registered?
A: Yes, registered with the Sri Lanka Export Development Board and compliant with ISO 22000 and HACCP standards.
"""

docs["faq_international_shipping.md"] = """# International Shipping FAQ
Q: Which incoterms do you support?
A: FOB Colombo is standard; CIF and DDP can be arranged on request with corresponding price adjustments.

Q: Do you handle customs clearance at the destination?
A: Under FOB and CIF terms, destination customs clearance is the buyer's responsibility. Under DDP terms, we arrange clearance via our logistics partners, though buyer-side import licenses (where required) remain the buyer's responsibility.

Q: What happens if my shipment is delayed at origin?
A: Delays are communicated proactively; for delays exceeding 10 working days beyond the quoted lead time, buyers are offered either a partial pre-shipment or a price review if raw material costs have changed materially.

Q: Can shipments be tracked?
A: Yes, a Bill of Lading / Airway Bill number is provided once cargo is booked, along with the shipping line's tracking portal link.

Q: Do you ship to landlocked or remote destinations?
A: Yes, via transshipment through nearby ports, though this typically adds 5-15 days to standard lead times.
"""

docs["faq_bulk_orders.md"] = """# Bulk & Container Orders FAQ
Q: What container sizes are typically used?
A: 20ft containers hold approximately 18-20 tonnes of bagged spices; 40ft containers hold approximately 26-28 tonnes, though tea (being lighter) may be volume-constrained before reaching weight capacity.

Q: Can I mix multiple products in one container?
A: Yes, mixed containers are common and accepted for combined order values above USD 3,000, subject to compatible storage requirements (e.g. vanilla requires refrigerated handling and may need separate arrangements).

Q: Do you offer discounts for container-load (FCL) orders?
A: Yes, FCL orders typically receive 8-15% preferential pricing versus LCL (less than container load) equivalents, reflecting reduced per-unit handling costs.

Q: How far in advance should I place a container order for seasonal items like cardamom?
A: At least one full harvest season ahead (i.e. book by September for October-February harvest) is strongly recommended given limited seasonal stock.

Q: What is the typical total lead time from order confirmation to vessel departure for a full container?
A: 20-35 working days depending on product mix, with cardamom, vanilla, and custom packaging orders at the longer end of that range.
"""

for fname, content in docs.items():
    with open(os.path.join(KB, fname), "w") as f:
        f.write(content.strip() + "\n")

print(f"Wrote {len(docs)} knowledge base documents to {KB}/")
