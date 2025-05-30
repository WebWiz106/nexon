from pymongo import MongoClient

# Initialize MongoDB client and database
# client = MongoClient("mongodb://localhost:27017/")
# db = client["your_database_name"]


class Careers:
    def __init__(
        self,
        domain,
        name,
        email,
        number,
        jobtitle,
        linkedin,
        resume_url,
        experience,
        skills,
        portfolio,
        cover_letter,
    ):
        # if not all([domain, name, email, number, jobtitle, linkedin, resume_url, experience, skills, portfolio, cover_letter]):
        #     raise ValueError("All fields must be filled")

        self.domain = domain
        self.name = name
        self.email = email
        self.number = number
        self.jobtitle = jobtitle
        self.linkedin = linkedin
        self.resume_url = resume_url
        self.experience = experience
        self.skills = skills
        self.portfolio = portfolio
        self.cover_letter = cover_letter

    def to_dict(Careers):
        return {
            "domain": Careers.domain,
            "name": Careers.name,
            "email": Careers.email,
            "number": Careers.number,
            "jobtitle": Careers.jobtitle,
            "linkedin": Careers.linkedin,
            "resume_url": Careers.resume_url,
            "experience": Careers.experience,
            "skills": Careers.skills,
            "portfolio": Careers.portfolio,
            "cover_letter": Careers.cover_letter,
        }

    def from_dict(career_dict):
        return Careers(
            domain=career_dict.get("domain"),
            name=career_dict.get("name"),
            email=career_dict.get("email"),
            number=career_dict.get("number"),
            jobtitle=career_dict.get("jobtitle"),
            linkedin=career_dict.get("linkedin"),
            resume_url=career_dict.get("resume_url"),
            experience=career_dict.get("experience"),
            skills=career_dict.get("skills"),
            portfolio=career_dict.get("portfolio"),
            cover_letter=career_dict.get("cover_letter"),
        )
