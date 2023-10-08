import datetime
import re

from profile_schema import Experience
from enums import EU_COUNTRIES, FAANG
from enums import PyDevReqs, UxDesignReqs


class BaseProfile:
    def __init__(self, profile):
        self.profile = profile
        self.profile.experiences.sort(key=lambda date: (
            date.starts_at, date.ends_at if date.ends_at else datetime.datetime.date(datetime.datetime.now())))
        if profile.experiences[-1].ends_at is None:
            self.profile.experiences[-1].ends_at = datetime.datetime.date(datetime.datetime.now())

    match = True
    reason = []

    def _get_years_for_all_experience(self) -> int:
        work_days = 0
        if len(self.profile.experiences) > 1:
            for i in range(len(self.profile.experiences) - 1):
                job = self.profile.experiences
                if job[i].ends_at > job[i + 1].starts_at:
                    work_days += abs(job[i + 1].ends_at - job[i].starts_at).days
                else:
                    work_days += abs(job[i].ends_at - job[i].starts_at).days

        last_job = self.profile.experiences[-1]
        if not last_job.ends_at:
            last_job.ends_at = datetime.datetime.date(datetime.datetime.now())
        work_days += (last_job.ends_at - last_job.starts_at).days

        return work_days // 365


class UXProfile(BaseProfile):

    @staticmethod
    def _get_years_from_one_position(position: Experience) -> int:
        start_date = position.starts_at
        end_date = position.ends_at if position.ends_at else datetime.datetime.date(datetime.datetime.now())
        return (end_date - start_date).days // 365

    def check_position(self):
        # На двух(или одном если компания одна) последних местах работал: Product designer или UX-designer или подобное
        last_two_jobs = self.profile.experiences[:2] \
            if len(self.profile.experiences) > 1 else self.profile.experiences

        for job in last_two_jobs:
            # уточнить регулярку
            if re.match("|".join(UxDesignReqs.POSITION), job.job_title, flags=re.IGNORECASE):
                self.match = True
            else:
                self.match = False
                self.reason.append(f"{UxDesignReqs.POSITION} was not found on last two jobs")

    def check_required_skills(self):
        # Владеет Figma, Sketch, UX-research, Miro(Любыми двумя)
        count_skills = 0
        for skill in UxDesignReqs.SKILLS:
            if re.match(skill, ", ".join(self.profile.skills), flags=re.IGNORECASE):
                count_skills += 1

        if count_skills >= UxDesignReqs.SKILLS_COUNT:
            self.match = True
        else:
            self.match = False
            # переделать
            self.reason.append(f"{UxDesignReqs.SKILLS} was not found")

    def check_country(self):
        # Живет в евросоюзе
        if self.profile.location.country in EU_COUNTRIES:
            self.match = True
        else:
            self.match = False
            self.reason.append("person was not living in EU")

    def check_experience_on_last_job(self):
        # Опыт на последнем месте работы более двух лет
        last_job = self.profile.experiences[-1]
        if self._get_years_from_one_position(last_job) > UxDesignReqs.LAST_EXPERIENCE:
            self.match = True
        else:
            self.match = False
            self.reason.append(f"experience less than {UxDesignReqs.LAST_EXPERIENCE} years on last job")

    def check_summary_experience(self):
        # Общий опыт менее пяти лет
        if self._get_years_for_all_experience() < UxDesignReqs.MAX_EXPERIENCE:
            self.match = True
        else:
            self.match = False
            self.reason.append(f"summary experience more than {UxDesignReqs.MAX_EXPERIENCE} years")

    def make_filter(self):
        self.check_position()
        self.check_required_skills()
        self.check_country()
        self.check_experience_on_last_job()
        self.check_summary_experience()
        return self.match, self.reason


class PyDevProfile(BaseProfile):

    def check_company(self):
        # Работал в FAANG на одном из последних двух местах работы
        last_two_jobs = self.profile.experiences[:-2]
        for job in last_two_jobs:
            if job.company_name.lower() in FAANG:
                self.match = True
            else:
                self.match = False
                self.reason.append(f"{FAANG} was not found on last two jobs")

    def check_position(self):
        # Должность на трех последних местах Backend developer или Software engineer
        last_tree_jobs = self.profile.experiences[:-3]
        for job in last_tree_jobs:
            if re.match("|".join(PyDevReqs.POSITION), job.job_title, flags=re.IGNORECASE):
                self.match = False
                self.reason.append(f"{PyDevReqs.POSITION} was not found on {job.job_title}")
                return
            else:
                self.match = True

    def check_summary_experience(self):
        # Общий опыт более 8 лет
        if self._get_years_for_all_experience() > PyDevReqs.MIN_EXPERIENCE:
            self.match = True
        else:
            self.match = False
            self.reason.append(f"summary experience less than {PyDevReqs.MIN_EXPERIENCE} years")

    def check_last_job_skills(self):
        # На последнем месте работал с python и c++
        last_job = self.profile.experiences[-1]
        skills_one_line = ", ".join(last_job.skills)
        for skill in PyDevReqs.LAST_JOB_SKILLS:
            if not re.match(skill, skills_one_line, flags=re.IGNORECASE):
                self.match = False
                self.reason.append(f"one is requirement skills: {skill} was not found on last job")
                return
            else:
                self.match = True

    def check_city(self):
        #  Живет в Лондоне
        if self.profile.location.city.lower() == PyDevReqs.CITY:
            self.match = True
        else:
            self.match = False
            self.reason.append(f"person was not live in {PyDevReqs.CITY}")

    def make_filter(self):
        self.check_company()
        self.check_position()
        self.check_summary_experience()
        self.check_last_job_skills()
        self.check_city()
        return self.match, self.reason
