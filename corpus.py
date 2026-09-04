# corpus.py
GOLD_CORPUS = [
    {
        "doc_id": "PA1970_S3p",
        "title": "The Patents Act, 1970",
        "section": "Section 3(p)",
        "heading": "Inventions Not Patentable - Traditional Knowledge",
        "jurisdiction": "India",
        "domain": "Patents",
        "formulation_relevance": ["classical", "proprietary"],
        "confidence_base": 0.98,
        "text": (
            "Section 3(p): The following are not inventions within the meaning of this Act: "
            "an invention which in effect, is traditional knowledge or which is an aggregation "
            "or duplication of known properties of traditionally known component or components. "
            "Traditional knowledge associated with Ayurvedic, Siddha, or Unani medicine cannot be "
            "patented in India unless there is substantial novelty and unexpected synergistic effect."
        )
    },
    {
        "doc_id": "PA1970_S3e",
        "title": "The Patents Act, 1970",
        "section": "Section 3(e)",
        "heading": "Mere Admixture Not Patentable",
        "jurisdiction": "India",
        "domain": "Patents",
        "formulation_relevance": ["classical", "proprietary"],
        "confidence_base": 0.95,
        "text": (
            "Section 3(e): A substance obtained by a mere admixture resulting only in the aggregation "
            "of the properties of the components thereof or a process for producing such substance is not patentable. "
            "Synergism must be demonstrated with experimental pharmacological data for Ayurvedic combinations."
        )
    },
    {
        "doc_id": "BDA2023_S6",
        "title": "Biological Diversity (Amendment) Act, 2023",
        "section": "Section 6",
        "heading": "Prior Approval for IPR Application",
        "jurisdiction": "India",
        "domain": "ABS/Biodiversity",
        "formulation_relevance": ["classical", "proprietary", "phytopharmaceutical"],
        "confidence_base": 0.96,
        "text": (
            "Section 6: No person shall apply for any intellectual property right, by whatever name called, "
            "in or outside India for any invention based on any research or information on a biological resource "
            "obtained from India, without obtaining the previous approval of the National Biodiversity Authority (NBA) "
            "before grant of such intellectual property right. AYUSH practitioners and cultivated resources have "
            "exemptions under specified conditions."
        )
    },
    {
        "doc_id": "DCA1940_CH4A",
        "title": "Drugs and Cosmetics Act, 1940",
        "section": "Section 33EEB",
        "heading": "Regulation of Ayurvedic, Siddha and Unani Drugs",
        "jurisdiction": "India",
        "domain": "Drug Classification",
        "formulation_relevance": ["classical", "proprietary"],
        "confidence_base": 0.95,
        "text": (
            "Section 33EEB: Classical Ayurvedic medicines must be manufactured strictly according to the formulae "
            "prescribed in the authoritative books specified in the First Schedule. Patent or Proprietary Ayurvedic "
            "medicines may contain ingredients mentioned in the classical texts but in novel formulations, requiring "
            "licensing under Rule 158B of Drugs Rules 1945."
        )
    },
    {
        "doc_id": "WIPO_GRATK_2024",
        "title": "WIPO Treaty on IP, Genetic Resources and Associated Traditional Knowledge (2024)",
        "section": "Article 3",
        "heading": "Mandatory Disclosure Requirement",
        "jurisdiction": "International",
        "domain": "International Treaty",
        "formulation_relevance": ["classical", "proprietary", "phytopharmaceutical"],
        "confidence_base": 0.94,
        "text": (
            "Article 3: Contracting Parties shall require patent applicants to disclose the country of origin "
            "of the genetic resources if the claimed invention is materially based on genetic resources. "
            "Where the claimed invention is materially based on traditional knowledge associated with genetic resources, "
            "the applicant must disclose the Indigenous Peoples or local community that provided the knowledge."
        )
    },
    {
        "doc_id": "TRIPS_ART27",
        "title": "TRIPS Agreement (WTO/WIPO)",
        "section": "Article 27.3(b)",
        "heading": "Patentable Subject Matter and Exclusions",
        "jurisdiction": "International",
        "domain": "International Treaty",
        "formulation_relevance": ["phytopharmaceutical", "proprietary"],
        "confidence_base": 0.92,
        "text": (
            "Article 27.3(b): Members may exclude from patentability plants and animals other than micro-organisms, "
            "and essentially biological processes for the production of plants or animals. However, microbiological "
            "processes and plant varieties must be protected either by patents or by an effective sui generis system."
        )
    }
]
