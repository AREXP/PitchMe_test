import datetime
import re

from profile_schema import Experience
from enums import EU_COUNTRIES, FAANG
from enums import PyDevReqs, UxDesignReqs


class BaseProfile:
    def __init__(self, profile):
        self.profile = profile
        self.profile.experiences.sort(key=lambda date: (date.starts_at, date.ends_at))
        self.reason = []
        self.match = True

    def _get_years_for_all_experience(self) -> int:
        work_days = 0
        if len(self.profile.experiences) > 1:
            for i in range(len(self.profile.experiences) - 1):
                job = self.profile.experiences
                if job[i].ends_at > job[i + 1].starts_at:
                    work_days += (job[i + 1].ends_at - job[i].starts_at).days
                else:
                    work_days += (job[i].ends_at - job[i].starts_at).days

        last_job = self.profile.experiences[-1]
        if not last_job.ends_at:
            last_job.ends_at = datetime.datetime.date(datetime.datetime.now())
        work_days += (last_job.ends_at - last_job.starts_at).days

        return work_days // 365

    def print_result(self):
        if len(self.reason) > 0:
            return f"{self.match}, {self.reason[0]}"
        return self.match


class UXProfile(BaseProfile):

    @staticmethod
    def _get_years_from_one_position(position: Experience) -> int:
        """
        return count of years on specified job

        :param position: specified position
        :return: return count of years
        """
        start_date = position.starts_at
        end_date = position.ends_at if position.ends_at else datetime.datetime.date(datetime.datetime.now())
        return (end_date - start_date).days // 365

    def _check_position_title(self):
        """ check the presence of required title jobs (Product designer, UX-designer or similar) on
        last two (ore one if not any) jobs"""
        # На двух(или одном если компания одна) последних местах работал: Product designer или UX-designer или подобное
        last_jobs = self.profile.experiences[-UxDesignReqs.POSITION_COUNT:] \
            if len(self.profile.experiences) > 1 else self.profile.experiences

        for job in last_jobs:
            pattern = re.compile(fr"\b({'|'.join(UxDesignReqs.POSITION)})", flags=re.IGNORECASE)
            if re.search(pattern, job.job_title) is None:
                self.match = False
                self.reason.append(f"{UxDesignReqs.POSITION} was not found on job: "
                                   f"{job.ends_at} - {job.starts_at} ({job.company_name} - {job.job_title})")
                return

    def _check_required_skills(self):
        """ check the presence of two required skills from list (Figma, Sketch, UX-research, Miro)"""
        # Владеет Figma, Sketch, UX-research, Miro(Любыми двумя)
        count_skills = 0
        for skill in UxDesignReqs.SKILLS:
            pattern = re.compile(fr"\b{skill}", flags=re.IGNORECASE)
            if re.search(pattern, ", ".join(self.profile.skills)):
                count_skills += 1

        if count_skills < UxDesignReqs.SKILLS_COUNT:
            self.match = False
            self.reason.append(f"Count of required skills: {count_skills} less "
                               f"than required {UxDesignReqs.SKILLS_COUNT} in profile skills {self.profile.skills}")

    def _check_country(self):
        """ check the presence country in EU countries"""
        if self.profile.location.country.lower() not in EU_COUNTRIES:
            self.match = False
            self.reason.append("Person was not living non of one EU country")

    def _check_experience_on_last_job(self):
        """ check count of years experience on last job position """
        last_job = self.profile.experiences[-1]
        if self._get_years_from_one_position(last_job) < UxDesignReqs.LAST_EXPERIENCE:
            self.match = False
            self.reason.append(f"Experience on last job less than required {UxDesignReqs.LAST_EXPERIENCE} years")

    def _check_summary_experience(self):
        """ check summary experience less than required years """
        if self._get_years_for_all_experience() > UxDesignReqs.MAX_EXPERIENCE:
            self.match = False
            self.reason.append(f"Summary experience more than required {UxDesignReqs.MAX_EXPERIENCE} years")

    def make_filter(self):
        """ run filters """
        self._check_position_title()
        self._check_required_skills()
        self._check_country()
        self._check_experience_on_last_job()
        self._check_summary_experience()


class PyDevProfile(BaseProfile):

    def _check_company(self):
        """ check the presence of FAANG in one of the last two jobs"""
        # Работал в FAANG на одном из последних двух местах работы
        last_two_jobs = self.profile.experiences[-2:]
        for job in last_two_jobs:
            if job.company_name.lower() not in FAANG:
                self.match = False
                self.reason.append(f"{FAANG} was not found on last two jobs")

    def _check_position_title(self):
        """ check the presence of position names (Backend Developer, Software Engineer) on last 3 jobs"""
        # Должность на трех последних местах Backend developer или Software engineer
        if len(self.profile.experiences) < PyDevReqs.POSITION_COUNT:
            self.match = False
            self.reason.append(f"Count of positions less than {PyDevReqs.POSITION_COUNT}. "
                               f"Titles of job cannot be checked")
            return
        last_tree_jobs = self.profile.experiences[-PyDevReqs.POSITION_COUNT:]
        for job in last_tree_jobs:
            pattern = re.compile(fr"\b({'|'.join(PyDevReqs.POSITION)})", flags=re.IGNORECASE)
            if re.search(pattern, job.job_title) is None:
                self.match = False
                self.reason.append(f"{PyDevReqs.POSITION} was not found on period: "
                                   f"{job.ends_at} - {job.starts_at} ({job.company_name} - {job.job_title})")
                return

    def _check_summary_experience(self):
        """ check summary experience more than 8 years"""
        if self._get_years_for_all_experience() < PyDevReqs.MIN_EXPERIENCE:
            self.match = False
            self.reason.append(f"Summary experience less than {PyDevReqs.MIN_EXPERIENCE} years")

    def _check_last_job_skills(self):
        """ check the presence of requirement skills (Python, C++) on last position """
        last_job = self.profile.experiences[-1]
        skills_one_line = ", ".join(last_job.skills)
        for skill in PyDevReqs.LAST_JOB_SKILLS:
            pattern = re.compile(fr"\b{re.escape(skill)}", flags=re.IGNORECASE)
            if re.search(pattern, skills_one_line) is None:
                self.match = False
                self.reason.append(f"One of requirement skills ({skill}) was not found on last job position: "
                                   f"{last_job.ends_at} - {last_job.starts_at} ({last_job.company_name} "
                                   f"- {last_job.job_title})")
                return

    def _check_city(self):
        """ check required city (London) in profile """
        if self.profile.location.city.lower() != PyDevReqs.CITY:
            self.match = False
            self.reason.append(f"Wrong city on profile: {self.profile.location.city}. "
                               f"Expected: {PyDevReqs.CITY}")

    def make_filter(self):
        """ run filters """
        self._check_company()
        self._check_position_title()
        self._check_summary_experience()
        self._check_last_job_skills()
        self._check_city()

