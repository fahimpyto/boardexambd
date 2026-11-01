"""Central SEO data for BoardExamBD.

Everything that changes per page lives here: metadata, FAQs, related links,
sources and review dates. HTML pages are generated/updated from this file.
"""

def page_path(file_name: str) -> str:
    """Return the public URL path for a generated HTML file."""
    if file_name == "index.html":
        return "/"
    return "/" + file_name.removesuffix(".html")


SITE = {
    "name": "BoardExamBD",
    "legal_name": "BoardExamBD",
    "domain": "https://boardexambd.com",
    "author": "BoardExamBD Editorial Team",
    "description": (
        "BoardExamBD publishes clear, verified guides to SSC, HSC and university "
        "admission notices, routines, results and form fill-up dates in Bangladesh."
    ),
    "language": "en",
    "theme_color": "#4F46E5",
    "og_image": "https://boardexambd.com/assets/images/og-default.jpg",
    "og_image_path": "assets/images/og-default.jpg",
    "logo": "https://boardexambd.com/assets/images/favicon-512x512.png",
    "twitter_card": "summary_large_image",
    "github": "https://github.com/fahimpyto/boardexambd",
}

HOME = {
    "file": "index.html",
    "slug": "home",
    "type": "Home",
    "cluster": "Home",
    "url": "https://boardexambd.com/",
    "title": "SSC, HSC & Admission Notices 2026 | BoardExamBD",
    "description": (
        "Latest SSC, HSC and university admission notices, routines, results and "
        "form fill-up dates for Bangladesh — verified and explained simply."
    ),
    "h1": "SSC, HSC & Admission Notices and Routines in Bangladesh",
    "published": "2026-10-26",
    "modified": "2026-10-31",
    "keywords": "SSC notices, HSC notices, university admission Bangladesh, exam routines 2026",
    "schema": "WebSite + Organization + WebPage",
    "next_review": "2026-11-15",
    "notes": "Homepage; no breadcrumb schema.",
}

BLOG = {
    "file": "blog.html",
    "slug": "blog",
    "type": "Blog hub",
    "cluster": "Blog",
    "url": "https://boardexambd.com/blog",
    "title": "SSC, HSC & Admission Guides 2026 | BoardExamBD",
    "description": (
        "All BoardExamBD guides — SSC and HSC routines, results, form fill-up, and "
        "university admission dates for Bangladesh, explained simply."
    ),
    "h1": "SSC, HSC & Admission Guides",
    "published": "2026-10-26",
    "modified": "2026-10-31",
    "keywords": "SSC guides, HSC guides, university admission guides Bangladesh",
    "schema": "CollectionPage + ItemList + BreadcrumbList",
    "next_review": "2026-11-15",
    "notes": "Article hub; grouped by SSC, HSC and Admission.",
}

NOT_FOUND = {
    "file": "404.html",
    "slug": "404",
    "type": "Utility",
    "cluster": "Utility",
    "url": "https://boardexambd.com/404",
    "title": "Page Not Found | BoardExamBD",
    "description": "The page you requested could not be found. Browse SSC, HSC and university admission guides on BoardExamBD.",
    "h1": "Page not found",
    "published": "2026-10-26",
    "modified": "2026-10-26",
    "keywords": "",
    "schema": "WebPage",
    "next_review": "",
    "notes": "noindex utility page.",
    "noindex": True,
    "indexable": False,
}

HUBS = [
    {
        "file": "ssc.html",
        "slug": "ssc",
        "type": "Category hub",
        "cluster": "SSC",
        "url": "https://boardexambd.com/ssc",
        "title": "SSC Notices & Routine 2026 — All Boards | BoardExamBD",
        "description": (
            "SSC exam notices, routine, result and form fill-up updates for all "
            "Bangladesh education boards — clear dates and official links."
        ),
        "h1": "SSC Notices & Routine 2026",
        "published": "2026-10-26",
        "modified": "2026-10-26",
        "keywords": "SSC notices 2026, SSC routine 2026, SSC result 2026, SSC form fill-up 2027",
        "schema": "CollectionPage + ItemList + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Rebuilt hub with verified SSC dates, guide cards, timeline and FAQs.",
        "faqs": [
            {
                "q": "When is the SSC 2026 exam?",
                "a": "The SSC 2026 written exams began on 11 April 2026 with the Bangla 1st paper. Every exam started at 10:00 AM, and the boards' full subject-wise schedule is in our SSC 2026 routine guide.",
            },
            {
                "q": "When was the SSC result 2026 published?",
                "a": "The SSC, Dakhil and Vocational results for 2026 were published on 10 August 2026 at 10:00 AM. Students could check the full marksheet online, by SMS or at their school.",
            },
            {
                "q": "When is SSC form fill-up 2027?",
                "a": "The boards announced SSC 2027 form fill-up from 16 to 23 November 2026 without a late fee. The process runs through each school, which submits candidate data to the board.",
            },
        ],
    },
    {
        "file": "hsc.html",
        "slug": "hsc",
        "type": "Category hub",
        "cluster": "HSC",
        "url": "https://boardexambd.com/hsc",
        "title": "HSC Notices & Routine 2026 — All Boards | BoardExamBD",
        "description": (
            "HSC exam notices, routine, result, form fill-up and practical exam "
            "updates for all Bangladesh education boards — explained simply."
        ),
        "h1": "HSC Notices & Routine 2026",
        "published": "2026-10-26",
        "modified": "2026-10-31",
        "keywords": "HSC notices 2026, HSC routine 2026, HSC result 2026, HSC form fill-up 2027",
        "schema": "CollectionPage + ItemList + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Rebuilt hub with verified SSC dates, guide cards, timeline and FAQs.",
        "faqs": [
            {
                "q": "When did the HSC 2026 exams start?",
                "a": "The HSC, Alim and equivalent written exams began on 2 July 2026 with the Bangla 1st paper. The written part ended on 8 August 2026, and practical exams were completed by 15 August 2026.",
            },
            {
                "q": "When was the HSC result 2026 published?",
                "a": "The HSC, Alim and DIBS results were published on Saturday, 31 October 2026, according to the education boards' latest notice. Check the official board portals or our HSC result guide for the exact steps.",
            },
            {
                "q": "When is HSC form fill-up 2027?",
                "a": "No 2027 circular had been issued as of 23 October 2026. Based on the 2026 cycle, the next form fill-up window is expected around February to March 2027 and will run through each college.",
            },
        ],
    },
    {
        "file": "admission.html",
        "slug": "admission",
        "type": "Category hub",
        "cluster": "Admission",
        "url": "https://boardexambd.com/admission",
        "title": "University Admission 2026-27 Notices | BoardExamBD",
        "description": (
            "University admission notices for 2026-27 — DU, BUET, medical, GST, RU, "
            "RUET, KU and SUST application dates, tests and requirements."
        ),
        "h1": "University Admission Notices 2026-27",
        "published": "2026-10-26",
        "modified": "2026-10-26",
        "keywords": "university admission 2026-27, DU admission, BUET admission, medical admission, GST admission",
        "schema": "CollectionPage + ItemList + BreadcrumbList + FAQPage",
        "next_review": "2026-11-10",
        "notes": "Rebuilt hub with verified admission tracker, guide cards and FAQs.",
        "faqs": [
            {
                "q": "When do university admission applications open for 2026-27?",
                "a": "The dates differ by university. DU applications run from 11 to 25 November 2026, RU opens on 12 November 2026, and BUET applications are expected from mid-November to early December 2026. Each university's official circular is final.",
            },
            {
                "q": "Which admission tests are coming next?",
                "a": "The medical admission test is tentatively set for 4 December 2026, DU unit tests run from 5 to 26 December 2026, BUET's preliminary test is on 16 January 2027, and RU unit tests are planned for 8, 9 and 16 January 2027.",
            },
            {
                "q": "Where should I verify admission dates?",
                "a": "Always verify with the official university or cluster portal — for example admission.eis.du.ac.bd, buet.ac.bd, dgme.teletalk.com.bd, gstadmission.ac.bd or admission.ru.ac.bd. BoardExamBD summarises the notices but is not an official source.",
            },
        ],
    },
]

ARTICLES = [
    {
        "file": "ssc-2026-routine.html",
        "slug": "ssc-2026-routine",
        "type": "Article",
        "cluster": "SSC",
        "category": "SSC",
        "category_url": "ssc",
        "url": "https://boardexambd.com/ssc-2026-routine",
        "title": "SSC 2026 Routine — Full Exam Schedule | BoardExamBD",
        "description": (
            "SSC 2026 exam routine with subject-wise dates, subject codes, 10:00 AM "
            "start time and official board instructions for all general boards."
        ),
        "h1": "SSC 2026 Exam Routine — Full Schedule & Details",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "SSC routine 2026, SSC exam schedule 2026, SSC exam date, Bangladesh education board",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Original routine notice preserved with images and rules.",
        "related": ["ssc-2026-result", "ssc-form-fillup-2027", "ssc-board-challenge-2026"],
        "sources": [
            ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
            ("Dhaka Education Board", "https://dhakaeducationboard.gov.bd/"),
        ],
        "checklist": [
            "Confirm your subject-wise dates on the official board routine.",
            "Reach the exam centre by 9:30 AM — every paper starts at 10:00 AM.",
            "Carry your admit card and registration card to every exam.",
            "Leave mobile phones and unauthorised calculators outside the hall.",
            "Re-check the board notice before each exam in case the routine changes.",
        ],
        "faqs": [
            {
                "q": "When does the SSC 2026 exam start?",
                "a": "The SSC 2026 exams begin on 11 April 2026 with the Bangla 1st paper. Every paper starts at 10:00 AM.",
            },
            {
                "q": "What time do SSC 2026 exams start?",
                "a": "All SSC 2026 exams start at 10:00 AM. Students should be seated in the exam hall by 9:30 AM.",
            },
            {
                "q": "Which boards follow this SSC routine?",
                "a": "This routine applies to the nine general education boards — Dhaka, Rajshahi, Cumilla, Jashore, Barishal, Sylhet, Dinajpur, Chattogram and Mymensingh. Madrasah and Technical board candidates follow their own notices.",
            },
            {
                "q": "Can the SSC 2026 routine change?",
                "a": "Yes. The education boards can change the routine if needed, so check your board's official notice before each exam.",
            },
        ],
    },
    {
        "file": "ssc-2026-result.html",
        "slug": "ssc-2026-result",
        "type": "Article",
        "cluster": "SSC",
        "category": "SSC",
        "category_url": "ssc",
        "url": "https://boardexambd.com/ssc-2026-result",
        "title": "SSC Result 2026 — Date & How to Check | BoardExamBD",
        "description": (
            "SSC and Dakhil result 2026 was published on 10 August. Check your "
            "marksheet online, by SMS or at school with this step-by-step guide."
        ),
        "h1": "SSC Result 2026 — Date & How to Check Online & SMS",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "SSC result 2026, SSC result check online, SSC result SMS, educationboardresults",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Result already published; keep steps and SMS format.",
        "related": ["ssc-2026-routine", "ssc-board-challenge-2026", "ssc-form-fillup-2027"],
        "sources": [
            ("Education Board Results", "https://www.educationboardresults.gov.bd/"),
            ("eBoard Results", "https://eboardresults.com/"),
        ],
        "checklist": [
            "Keep your exam roll and registration number ready.",
            "Try the official results portal first; use SMS if the site is busy.",
            "Use the correct three-letter board code, such as DHA or RAJ.",
            "Save or print the full marksheet after it opens.",
            "Check the board challenge window if you doubt a subject mark.",
        ],
        "faqs": [
            {
                "q": "When was the SSC result 2026 published?",
                "a": "The SSC, Dakhil and Vocational results for 2026 were published on 10 August 2026 at 10:00 AM.",
            },
            {
                "q": "How can I check my SSC result 2026 online?",
                "a": "Open educationboardresults.gov.bd, select SSC/Dakhil/Equivalent, choose 2026 and your board, then enter your exam roll and registration number.",
            },
            {
                "q": "What is the SMS format for SSC result 2026?",
                "a": "Send SSC <space> BOARD <space> ROLL <space> 2026 to 16222 or 16140. For example: SSC DHA 113456 2026.",
            },
            {
                "q": "Which exams are covered by the SSC 2026 result?",
                "a": "The result covers SSC, Dakhil and Vocational candidates across 11 education boards, including the nine general boards, the Madrasah board and the Technical board.",
            },
        ],
    },
    {
        "file": "ssc-form-fillup-2027.html",
        "slug": "ssc-form-fillup-2027",
        "type": "Article",
        "cluster": "SSC",
        "category": "SSC",
        "category_url": "ssc",
        "url": "https://boardexambd.com/ssc-form-fillup-2027",
        "title": "SSC Form Fill-up 2027 — Dates & Process | BoardExamBD",
        "description": (
            "SSC 2027 form fill-up runs through your institution. See the announced "
            "online window, fees, late fee rules and step-by-step process."
        ),
        "h1": "SSC Form Fill-up 2027 — Dates & How to Apply",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "SSC form fill-up 2027, SSC 2027 registration, SSC form fill-up date, SSC fee",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-24",
        "notes": "Critical date window 16–23 Nov 2026; update after it closes.",
        "related": ["ssc-2026-routine", "ssc-2026-result", "ssc-board-challenge-2026"],
        "sources": [
            ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
            ("Dhaka Education Board", "https://dhakaeducationboard.gov.bd/"),
        ],
        "checklist": [
            "Confirm your group, optional and practical subjects with your school.",
            "Complete the process within 16–23 November 2026 to avoid a late fee.",
            "Pay the board-set fee through your institution and keep the receipt.",
            "Check the printed form for name spelling, date of birth and photo.",
            "Ask your school about the late-fee window only if you miss the main dates.",
        ],
        "faqs": [
            {
                "q": "When is SSC form fill-up 2027?",
                "a": "The announced online window is 16–23 November 2026 without a late fee. The exact fee and late-fee dates are set in each board's notice.",
            },
            {
                "q": "Do students fill up the SSC 2027 form themselves?",
                "a": "No. The school uploads candidate data to the board's online system. Students confirm their subjects, pay the fee and verify the printed form at the institution.",
            },
            {
                "q": "What is the SSC 2027 form fill-up fee?",
                "a": "The fee is set by the education boards and paid through your school. Check your school's notice or the board circular for the exact amount.",
            },
            {
                "q": "What happens if I miss the 23 November deadline?",
                "a": "A late-fee window usually follows the main window, but it is harder and more expensive. Do not rely on it — finish the form fill-up within 16–23 November 2026.",
            },
        ],
    },
    {
        "file": "ssc-board-challenge-2026.html",
        "slug": "ssc-board-challenge-2026",
        "type": "Article",
        "cluster": "SSC",
        "category": "SSC",
        "category_url": "ssc",
        "url": "https://boardexambd.com/ssc-board-challenge-2026",
        "title": "SSC Board Challenge 2026 — Fees & Result | BoardExamBD",
        "description": (
            "SSC board challenge 2026 applications ran 11–17 August by SMS, Tk 150 "
            "per paper, results on 10 September. See the full process and next cycle."
        ),
        "h1": "SSC Board Challenge 2026 — Process, Fees & Result",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "SSC board challenge 2026, SSC re-scrutiny, board challenge fee, SSC challenge result",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "2026 cycle complete; next update after SSC 2027 result.",
        "related": ["ssc-2026-result", "ssc-2026-routine", "ssc-form-fillup-2027"],
        "sources": [
            ("Education Board Results", "https://www.educationboardresults.gov.bd/"),
            ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
        ],
        "checklist": [
            "Check your full marksheet before deciding to challenge a paper.",
            "Apply only if you believe a mark was missed or added incorrectly.",
            "Use your own pre-paid mobile number for the SMS application.",
            "Send the RSC format to 16222 and confirm the PIN when prompted.",
            "Save the confirmation SMS and check the challenge result online.",
        ],
        "faqs": [
            {
                "q": "What is the SSC board challenge?",
                "a": "The board challenge, or re-scrutiny, is a review of your answer scripts to check whether marks were missed or added incorrectly. It is not a re-examination.",
            },
            {
                "q": "When was the SSC board challenge 2026 window?",
                "a": "The 2026 re-scrutiny application window ran from 11 to 17 August 2026 and was completed by SMS.",
            },
            {
                "q": "How much did the SSC board challenge cost?",
                "a": "The fee was Tk 150 per paper. For subjects with two papers, the fee was charged for each paper, and the standard rule refunds the fee if marks increase.",
            },
            {
                "q": "When was the SSC board challenge result published?",
                "a": "The 2026 challenge results were published on 10 September 2026. The next cycle is expected after the SSC 2027 result.",
            },
        ],
    },
    {
        "file": "hsc-2026-routine.html",
        "slug": "hsc-2026-routine",
        "type": "Article",
        "cluster": "HSC",
        "category": "HSC",
        "category_url": "hsc",
        "url": "https://boardexambd.com/hsc-2026-routine",
        "title": "HSC Routine 2026 — Exam Dates & Schedule | BoardExamBD",
        "description": (
            "HSC 2026 routine with written exam dates from 2 July to 8 August, "
            "practical exams by 15 August, and exam times for all education boards."
        ),
        "h1": "HSC Routine 2026 — Exam Dates & Full Schedule",
        "published": "2026-10-23",
        "modified": "2026-10-31",
        "keywords": "HSC routine 2026, HSC exam date 2026, HSC schedule, Bangladesh education board",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Exams complete; keep timeline and result link current.",
        "related": ["hsc-2026-result", "hsc-form-fillup-2027", "hsc-practical-2026"],
        "sources": [
            ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
            ("Dhaka Education Board", "https://dhakaeducationboard.gov.bd/"),
        ],
        "checklist": [
            "Confirm your board's official subject-wise routine.",
            "Reach the centre by 9:30 AM for the 10:00 AM paper.",
            "Carry your admit card and registration card every day.",
            "Follow the board's rules on calculators and mobile phones.",
            "Watch for any routine change announced by your board.",
        ],
        "faqs": [
            {
                "q": "When did the HSC 2026 exams start?",
                "a": "The HSC, Alim and equivalent written exams began on 2 July 2026 with the Bangla 1st paper.",
            },
            {
                "q": "When did the HSC 2026 written exams end?",
                "a": "The written exams ended on 8 August 2026, and practical exams were completed by 15 August 2026.",
            },
            {
                "q": "What time did HSC 2026 exams start?",
                "a": "Every HSC 2026 exam started at 10:00 AM. Students were advised to be seated by 9:30 AM.",
            },
            {
                "q": "Which boards followed the HSC 2026 routine?",
                "a": "The routine covered 11 boards — nine general boards for HSC, the Madrasah board for Alim, and the Technical board for BM/DIBS candidates.",
            },
            {
                "q": "When was the HSC result 2026 published?",
                "a": "The HSC, Alim and DIBS results were published on Saturday, 31 October 2026, according to the latest board notice.",
            },
        ],
    },
    {
        "file": "hsc-2026-result.html",
        "slug": "hsc-2026-result",
        "type": "Article",
        "cluster": "HSC",
        "category": "HSC",
        "category_url": "hsc",
        "url": "https://boardexambd.com/hsc-2026-result",
        "title": "HSC Result 2026 — Date & How to Check | BoardExamBD",
        "description": (
            "HSC and Alim result 2026 was published 31 October 2026 (pass rate 52.12%, "
            "40,084 GPA-5). Check your marksheet online at eboardresults.com or by "
            "SMS with this simple guide."
        ),
        "h1": "HSC Result 2026 — Date & How to Check Online/SMS",
        "published": "2026-10-23",
        "modified": "2026-10-31",
        "keywords": "HSC result 2026, HSC result date, HSC result check online, HSC result SMS",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-07",
        "notes": "Result published 31 October 2026 (revised from 29 Oct); re-scrutiny window 1-7 Nov 2026.",
        "related": ["hsc-2026-routine", "hsc-practical-2026", "hsc-form-fillup-2027"],
        "sources": [
            ("Education Board Results", "https://www.educationboardresults.gov.bd/"),
            ("eBoard Results", "https://eboardresults.com/"),
        ],
        "checklist": [
            "Keep your HSC roll and registration number ready.",
            "Use the official board portal or eboardresults.com.",
            "Use the SMS format HSC <Board> <Roll> 2026 to 16140.",
            "Save or print the full marksheet.",
            "Check the re-scrutiny window if you doubt a mark.",
        ],
        "faqs": [
            {
                "q": "When was the HSC result 2026 published?",
                "a": "The HSC, Alim and DIBS results were published on Saturday, 31 October 2026, according to the education boards' latest notice.",
            },
            {
                "q": "How can I check the HSC result 2026 online?",
                "a": "Open educationboardresults.gov.bd or eboardresults.com, select HSC/Alim/Equivalent, choose 2026 and your board, then enter your roll and registration number.",
            },
            {
                "q": "What is the SMS format for the HSC result 2026?",
                "a": "Send HSC <space> BOARD <space> ROLL <space> 2026 to 16140. For example: HSC DHA 113456 2026.",
            },
            {
                "q": "Which exams are covered by the HSC 2026 result?",
                "a": "The result covers HSC, Alim and DIBS candidates across all 11 education boards on the same day.",
            },
        ],
    },
    {
        "file": "hsc-form-fillup-2027.html",
        "slug": "hsc-form-fillup-2027",
        "type": "Article",
        "cluster": "HSC",
        "category": "HSC",
        "category_url": "hsc",
        "url": "https://boardexambd.com/hsc-form-fillup-2027",
        "title": "HSC Form Fill-up 2027 — Dates & Process | BoardExamBD",
        "description": (
            "HSC form fill-up 2027 is expected around February–March. See how the "
            "college-based process works, the 2026 fees and what to prepare."
        ),
        "h1": "HSC Form Fill-up 2027 — Expected Dates & Process",
        "published": "2026-10-23",
        "modified": "2026-10-31",
        "keywords": "HSC form fill-up 2027, HSC 2027 registration, HSC form fill-up date, college form fill-up",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-12-15",
        "notes": "Expected window; update when the 2027 circular is published.",
        "related": ["hsc-2026-routine", "hsc-2026-result", "hsc-practical-2026"],
        "sources": [
            ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
            ("Dhaka Education Board", "https://dhakaeducationboard.gov.bd/"),
        ],
        "checklist": [
            "Confirm your subjects, optional paper and practical subjects with your college.",
            "Watch for the 2027 circular around February 2027.",
            "Pay the exam fee by the deadline set in the board circular.",
            "Verify your name, roll, registration and photo on the printed form.",
            "Keep the fee receipt for admit card and result collection.",
        ],
        "faqs": [
            {
                "q": "When is HSC form fill-up 2027?",
                "a": "No 2027 circular had been issued as of 23 October 2026. Based on the last cycle, the window is expected around February–March 2027.",
            },
            {
                "q": "When was the HSC 2026 form fill-up?",
                "a": "The 2026 online form fill-up ran from 1 to 9 March 2026, with fees due by 10 March and a late-fee extension to about 18 March.",
            },
            {
                "q": "How does the HSC form fill-up work?",
                "a": "The college uploads candidate data to the board's online system. Students confirm subjects, pay the fee and verify the printed form before the college finalises it.",
            },
            {
                "q": "What should I prepare for HSC form fill-up 2027?",
                "a": "Keep your registration information, subject list, photo and fee ready. Check the college notice and board circular for the exact documents and deadlines.",
            },
        ],
    },
    {
        "file": "hsc-practical-2026.html",
        "slug": "hsc-practical-2026",
        "type": "Article",
        "cluster": "HSC",
        "category": "HSC",
        "category_url": "hsc",
        "url": "https://boardexambd.com/hsc-practical-2026",
        "title": "HSC Practical Exams 2026 — Rules & Marks | BoardExamBD",
        "description": (
            "HSC 2026 practical exams were held at students' own institutions and "
            "completed by 15 August. See the schedule rules, marks and what to carry."
        ),
        "h1": "HSC Practical Exams 2026 — Schedule, Rules & Marks",
        "published": "2026-10-23",
        "modified": "2026-10-31",
        "keywords": "HSC practical exam 2026, HSC practical schedule, HSC practical marks, lab exam",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "2026 practical cycle complete; next update for 2027 batch.",
        "related": ["hsc-2026-routine", "hsc-2026-result", "hsc-form-fillup-2027"],
        "sources": [
            ("Education Board Bangladesh", "https://www.educationboard.gov.bd/"),
            ("Dhaka Education Board", "https://dhakaeducationboard.gov.bd/"),
        ],
        "checklist": [
            "Check your college notice board for your subject-wise practical dates.",
            "Carry your practical notebook and lab records.",
            "Bring your admit card and a photo ID to the practical centre.",
            "Follow lab safety and examiner instructions during the session.",
            "Confirm that your practical marks are forwarded with the theory marks.",
        ],
        "faqs": [
            {
                "q": "When were the HSC 2026 practical exams held?",
                "a": "The HSC 2026 practical exams were completed by 15 August 2026, after the written exams ended on 8 August.",
            },
            {
                "q": "Where were the HSC 2026 practical exams held?",
                "a": "Practicals were held at each student's own institution or assigned centre. Every college announced its own subject-wise and shift-wise dates.",
            },
            {
                "q": "Who takes the HSC practical exams?",
                "a": "Science group students take practicals in subjects such as Physics, Chemistry and Biology, along with practical or oral papers such as ICT. Alim and BM/DIBS candidates follow their own board arrangements.",
            },
            {
                "q": "Do HSC practical marks count in the final result?",
                "a": "Yes. Practical marks are merged with the theory marks for the subject and forwarded to the board for the final result.",
            },
        ],
    },
    {
        "file": "buet-admission-2026-27.html",
        "slug": "buet-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/buet-admission-2026-27",
        "title": "BUET Admission 2026-27 — Dates & Process | BoardExamBD",
        "description": (
            "BUET admission 2026-27 preliminary test is set for 16 January 2027. "
            "See application dates, eligibility, the two-phase test and official portal links."
        ),
        "h1": "BUET Admission 2026-27 — Application & Exam Date",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "BUET admission 2026-27, BUET admission test date, BUET application, BUET preliminary test",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-20",
        "notes": "Preliminary test confirmed 16 Jan 2027; application window expected.",
        "related": ["du-a-unit-admission-2026-27", "ruet-admission-2026-27", "medical-admission-2026-27"],
        "sources": [
            ("BUET", "https://www.buet.ac.bd/"),
            ("BUET Admission", "https://admission.buet.ac.bd/"),
        ],
        "checklist": [
            "Watch buet.ac.bd for the full 2026-27 circular.",
            "Confirm your eligible group and minimum GPA in the prospectus.",
            "Apply online and pay the application fee within the window.",
            "Download the admit card and check your centre.",
            "Prepare for both the preliminary MCQ and the written test.",
        ],
        "faqs": [
            {
                "q": "When is the BUET admission test 2026-27?",
                "a": "The BUET preliminary admission test is set for 16 January 2027. The written test for shortlisted candidates is expected about a month later.",
            },
            {
                "q": "When is the BUET application window?",
                "a": "BUET has not published the full circular yet. Based on the last cycle, online applications are expected from around mid-November to early December 2026.",
            },
            {
                "q": "What is the BUET admission test format?",
                "a": "BUET uses two phases: a preliminary MCQ test and a written test for shortlisted candidates. Final merit is drawn from the written test.",
            },
            {
                "q": "Where do I apply for BUET admission?",
                "a": "Apply on the official BUET admission site when the circular opens. The university's own prospectus is the final source for eligibility and fees.",
            },
        ],
    },
    {
        "file": "du-a-unit-admission-2026-27.html",
        "slug": "du-a-unit-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/du-a-unit-admission-2026-27",
        "title": "DU A Unit Admission 2026-27 — Dates | BoardExamBD",
        "description": (
            "DU A Unit admission 2026-27 applications run 11–25 November, with unit "
            "tests from 5–26 December. See eligibility, form fill-up and exam details."
        ),
        "h1": "DU A Unit Admission 2026-27 — Form Fill-up & Exam Date",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "DU A unit admission 2026-27, Dhaka University admission, DU admission test date, DU application",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-26",
        "notes": "Application window 11–25 Nov 2026; tests 5–26 Dec 2026.",
        "related": ["gst-a-unit-admission-2026-27", "buet-admission-2026-27", "ru-admission-2026-27"],
        "sources": [
            ("DU Admission Portal", "https://admission.eis.du.ac.bd/"),
            ("University of Dhaka", "https://www.du.ac.bd/"),
        ],
        "checklist": [
            "Check the A unit eligibility rules in the DU circular.",
            "Apply online between 11 and 25 November 2026.",
            "Pay the fee before 11:59 PM on 25 November.",
            "Download the admit card and check the seat plan.",
            "Carry the admit card and HSC registration card to the test.",
        ],
        "faqs": [
            {
                "q": "When is the DU A Unit application 2026-27?",
                "a": "DU A Unit applications open at 12:00 noon on 11 November 2026 and close at 11:59 PM on 25 November 2026.",
            },
            {
                "q": "When is the DU A Unit admission test?",
                "a": "All DU unit tests are scheduled between 5 and 26 December 2026. The exact A Unit date and seat plan are published on admission.eis.du.ac.bd.",
            },
            {
                "q": "What is the minimum GPA for DU A Unit?",
                "a": "The common requirement is a combined GPA of 8.00 in SSC and HSC, with at least 3.50 in each exam. Check the official circular for group-specific rules.",
            },
            {
                "q": "Where do I apply for DU A Unit admission?",
                "a": "Apply online at admission.eis.du.ac.bd. The portal also handles the admit card, seat plan and results.",
            },
        ],
    },
    {
        "file": "gst-a-unit-admission-2026-27.html",
        "slug": "gst-a-unit-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/gst-a-unit-admission-2026-27",
        "title": "GST Admission 2026-27 — A Unit Dates | BoardExamBD",
        "description": (
            "GST university cluster admission 2026-27 A Unit form fill-up, one-hour "
            "MCQ pattern, eligibility and the latest circular updates from gstadmission.ac.bd."
        ),
        "h1": "GST Admission 2026-27 — A Unit Form Fill-up & Exam Date",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "GST admission 2026-27, GST A unit, GST cluster admission, gstadmission.ac.bd",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Circular not published as of 23 Oct 2026; update when released.",
        "related": ["du-a-unit-admission-2026-27", "ru-admission-2026-27", "sust-admission-2026-27"],
        "sources": [
            ("GST Admission", "https://gstadmission.ac.bd/"),
        ],
        "checklist": [
            "Watch gstadmission.ac.bd for the 2026-27 circular.",
            "Confirm your unit and eligibility in the guideline.",
            "Apply once and pay the cluster application fee.",
            "Download the admit card before the test day.",
            "Check your merit position and submit the preference list.",
        ],
        "faqs": [
            {
                "q": "When will the GST 2026-27 circular be published?",
                "a": "The GST 2026-27 circular had not been published as of 23 October 2026. It is expected on gstadmission.ac.bd, with the application and test dates inside.",
            },
            {
                "q": "What is the GST admission test pattern?",
                "a": "GST uses a one-hour MCQ test held on Fridays from 11:00 AM to 12:00 PM, with separate test days for each unit.",
            },
            {
                "q": "What was the GST A Unit test date last cycle?",
                "a": "In the 2025-26 cycle, the GST A Unit science test was held on Friday, 10 April 2026.",
            },
            {
                "q": "What GPA is required for GST admission?",
                "a": "Last cycle's guideline required a minimum GPA of 3.50 in both SSC and HSC, including optional subjects. The 2026-27 circular is the final source.",
            },
        ],
    },
    {
        "file": "ku-admission-2026-27.html",
        "slug": "ku-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/ku-admission-2026-27",
        "title": "KU Admission 2026-27 — Application & Test | BoardExamBD",
        "description": (
            "Khulna University admission 2026-27 applications closed on 30 September. "
            "See the test schedule, eligibility and next steps on ku.ac.bd."
        ),
        "h1": "KU Admission 2026-27 — Application & Exam Date",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "KU admission 2026-27, Khulna University admission, KU admission test date",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Application closed 30 Sep 2026; test schedule pending on ku.ac.bd.",
        "related": ["ru-admission-2026-27", "sust-admission-2026-27", "ruet-admission-2026-27"],
        "sources": [
            ("Khulna University", "https://ku.ac.bd/"),
        ],
        "checklist": [
            "Note that the application window closed on 30 September 2026.",
            "Watch ku.ac.bd for the discipline-wise test schedule.",
            "Download and print the admit card when it opens.",
            "Carry the printed admit card and a photo ID to the test.",
            "Check the merit list and complete admission within the deadline.",
        ],
        "faqs": [
            {
                "q": "When was the KU admission 2026-27 application?",
                "a": "Khulna University accepted online applications from 1 to 30 September 2026. The window has now closed.",
            },
            {
                "q": "When is the KU admission test 2026-27?",
                "a": "KU announces discipline-wise test dates on ku.ac.bd. The schedule had not been published as of 23 October 2026.",
            },
            {
                "q": "When were the KU admission tests last cycle?",
                "a": "The 2025-26 admission tests were held on 18–19 December 2025. This cycle's official schedule may differ.",
            },
            {
                "q": "Can I still apply for KU admission 2026-27?",
                "a": "No. The application window closed on 30 September 2026, and late applications are not accepted. Watch ku.ac.bd for any official supplementary notice.",
            },
        ],
    },
    {
        "file": "medical-admission-2026-27.html",
        "slug": "medical-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/medical-admission-2026-27",
        "title": "Medical Admission 2026-27 — Dates & Process | BoardExamBD",
        "description": (
            "MBBS and BDS medical admission 2026-27: DGME form fill-up, tentative "
            "test date 4 December, eligibility and the one-hour MCQ exam format."
        ),
        "h1": "Medical (MBBS/BDS) Admission 2026-27 — Form Fill-up & Exam Date",
        "published": "2026-10-23",
        "modified": "2026-10-31",
        "keywords": "medical admission 2026-27, MBBS admission, BDS admission, DGME admission test",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Test tentative 4 Dec 2026; depends on HSC result published 31 Oct 2026.",
        "related": ["hsc-2026-result", "du-a-unit-admission-2026-27", "buet-admission-2026-27"],
        "sources": [
            ("DGME Admission", "https://dgme.teletalk.com.bd/"),
            ("Directorate General of Medical Education", "https://dgme.gov.bd/"),
        ],
        "checklist": [
            "Watch dgme.teletalk.com.bd for the official circular.",
            "Check the current GPA and quota rules in the circular.",
            "Fill the online form and pay the fee before the deadline.",
            "Download the admit card and check your centre.",
            "Prepare for the 100-mark MCQ test in 1 hour 15 minutes.",
        ],
        "faqs": [
            {
                "q": "When is the medical admission test 2026-27?",
                "a": "The MBBS/BDS admission test is tentatively set for 4 December 2026. The date depends on the HSC result and is confirmed only in the DGME circular.",
            },
            {
                "q": "When is the medical form fill-up 2026-27?",
                "a": "Form fill-up is expected around mid-November 2026 on dgme.teletalk.com.bd, matching the previous cycle's timing.",
            },
            {
                "q": "What is the medical admission test format?",
                "a": "The test is a 100-mark MCQ paper lasting 1 hour 15 minutes, covering Biology, Chemistry, Physics, English and General Knowledge.",
            },
            {
                "q": "What GPA is required for medical admission?",
                "a": "Last cycle's reported minimum was a combined SSC and HSC GPA of 8.50, with at least 3.50 in each exam. The 2026-27 circular is final.",
            },
        ],
    },
    {
        "file": "ru-admission-2026-27.html",
        "slug": "ru-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/ru-admission-2026-27",
        "title": "RU Admission 2026-27 — Application & Tests | BoardExamBD",
        "description": (
            "Rajshahi University admission 2026-27 applications open 12 November, "
            "with B, C and A unit tests in January 2027. See dates and eligibility."
        ),
        "h1": "Rajshahi University (RU) Admission 2026-27 — Dates & Process",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "RU admission 2026-27, Rajshahi University admission, RU admission test date",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-13",
        "notes": "Applications open 12 Nov 2026; tests 8, 9 and 16 Jan 2027.",
        "related": ["ruet-admission-2026-27", "ku-admission-2026-27", "sust-admission-2026-27"],
        "sources": [
            ("RU Admission Portal", "https://admission.ru.ac.bd/"),
            ("University of Rajshahi", "https://www.ru.ac.bd/"),
        ],
        "checklist": [
            "Choose the correct A, B or C unit for your HSC group.",
            "Apply from 12 November 2026 on admission.ru.ac.bd.",
            "Pay the fee for each unit you apply to.",
            "Download the admit card and check your campus room.",
            "Re-check the unit notice before the test in case dates change.",
        ],
        "faqs": [
            {
                "q": "When do RU admission applications open for 2026-27?",
                "a": "Rajshahi University preliminary applications open on 12 November 2026 at admission.ru.ac.bd.",
            },
            {
                "q": "When are the RU unit tests?",
                "a": "The initial schedule lists Unit B on 8 January 2027, Unit C on 9 January 2027 and Unit A on 16 January 2027.",
            },
            {
                "q": "Where do I apply for RU admission?",
                "a": "Apply on admission.ru.ac.bd. The portal also publishes unit notices, admit cards and results.",
            },
            {
                "q": "Is the RU admission schedule final?",
                "a": "The January dates are the initially announced schedule. Application deadlines, fees and any rescheduling are final only in the notices at admission.ru.ac.bd.",
            },
        ],
    },
    {
        "file": "ruet-admission-2026-27.html",
        "slug": "ruet-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/ruet-admission-2026-27",
        "title": "RUET Admission 2026-27 — Dates & Process | BoardExamBD",
        "description": (
            "RUET admission 2026-27 circular is expected in late November. See the "
            "application portal, eligibility, last cycle dates and what to prepare."
        ),
        "h1": "RUET Admission 2026-27 — Application & Exam Date",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "RUET admission 2026-27, RUET admission test date, RUET circular, admission.ruet.ac.bd",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-12-01",
        "notes": "Circular expected late Nov 2026; test expected Jan 2027.",
        "related": ["buet-admission-2026-27", "ku-admission-2026-27", "sust-admission-2026-27"],
        "sources": [
            ("RUET Admission", "https://admission.ruet.ac.bd/"),
            ("RUET", "https://www.ruet.ac.bd/"),
        ],
        "checklist": [
            "Watch admission.ruet.ac.bd for the 2026-27 circular.",
            "Read the prospectus for eligible groups and department seats.",
            "Apply online and pay the fee when the window opens.",
            "Download the admit card and check your centre.",
            "Prepare for the single MCQ science test.",
        ],
        "faqs": [
            {
                "q": "When will the RUET admission circular 2026-27 be published?",
                "a": "RUET's 2026-27 circular had not been published as of 23 October 2026. Based on last year, it is expected around late November or December 2026.",
            },
            {
                "q": "When is the RUET admission test 2026-27?",
                "a": "The test is expected around January 2027, following the pattern of the previous cycle.",
            },
            {
                "q": "What was the RUET admission schedule last cycle?",
                "a": "The 2025-26 circular was published on 25 November 2025, applications opened on 2 December 2025, the test was held in early January 2026, and results were expected around 6 February 2026.",
            },
            {
                "q": "What is the RUET admission test format?",
                "a": "RUET uses a single MCQ admission test covering science subjects. The prospectus lists eligible groups, minimum GPA requirements and department seats.",
            },
        ],
    },
    {
        "file": "sust-admission-2026-27.html",
        "slug": "sust-admission-2026-27",
        "type": "Article",
        "cluster": "Admission",
        "category": "Admission",
        "category_url": "admission",
        "url": "https://boardexambd.com/sust-admission-2026-27",
        "title": "SUST Admission 2026-27 — Dates & Process | BoardExamBD",
        "description": (
            "SUST admission 2026-27 A and B unit tests, application window on "
            "admission.sust.edu.bd, eligibility and the latest circular updates."
        ),
        "h1": "SUST Admission 2026-27 — Application & Exam Date",
        "published": "2026-10-23",
        "modified": "2026-10-23",
        "keywords": "SUST admission 2026-27, SUST admission test date, SUST A unit, SUST B unit",
        "schema": "Article + Organization + WebPage + BreadcrumbList + FAQPage",
        "next_review": "2026-11-15",
        "notes": "Circular expected late Oct–Nov 2026; test expected Dec 2026.",
        "related": ["ku-admission-2026-27", "ruet-admission-2026-27", "ru-admission-2026-27"],
        "sources": [
            ("SUST Admission", "https://admission.sust.edu.bd/"),
            ("Shahjalal University of Science and Technology", "https://www.sust.edu/"),
        ],
        "checklist": [
            "Read the SUST prospectus for unit and department criteria.",
            "Apply in the correct A or B unit.",
            "Pay the fee and download the admit card.",
            "Check your assigned test centre.",
            "Complete admission within the enrollment window if selected.",
        ],
        "faqs": [
            {
                "q": "When will the SUST admission circular 2026-27 be published?",
                "a": "The 2026-27 circular had not been published as of 23 October 2026. It is expected around late October or November 2026 on admission.sust.edu.bd.",
            },
            {
                "q": "When is the SUST admission test 2026-27?",
                "a": "The test is expected in December 2026. Last cycle, the A and B unit entry test was held on Sunday, 7 December 2025.",
            },
            {
                "q": "What are the SUST admission units?",
                "a": "SUST admits through the A unit for science and engineering, and the B unit for other disciplines. Each unit has a separate test and merit list.",
            },
            {
                "q": "What GPA is required for SUST admission?",
                "a": "SUST applies the common GPA rule plus department-specific criteria, such as a minimum GPA of 3.0 in individual requirements. The current prospectus is the final source.",
            },
        ],
    },
]

# Add common keys that are not repeated in every article.
for article in ARTICLES:
    article.setdefault("indexable", True)
    article.setdefault("noindex", False)
    article.setdefault("read_time", 6)

ALL_INDEXABLE = [HOME] + HUBS + [BLOG] + ARTICLES
ALL_PAGES = ALL_INDEXABLE + [NOT_FOUND]

# Public URLs are extensionless: /blog, /ssc-2026-routine, and / for the homepage.
for page in ALL_PAGES:
    page["path"] = page_path(page["file"])
    page["url"] = f"{SITE['domain']}{page['path']}"
for article in ARTICLES:
    article["category_url"] = article["category_url"].removesuffix(".html")

ARTICLE_BY_SLUG = {article["slug"]: article for article in ARTICLES}
PAGE_BY_FILE = {page["file"]: page for page in ALL_PAGES}
