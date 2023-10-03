from applicants.base import BaseApplicant
from profile_schema import Profile


class ExperiencePythonDeveloper(BaseApplicant):

    def __init__(self, profile: Profile) -> None:
        super().__init__(profile)
        self.expected_experience = 5
        self.expected_city = 'london'
        self.expected_companies = ['facebook', 'amazon', 'apple', 'netflix', 'google']
        self.expected_roles = ['backend developer', 'software engineer']
        self.expected_skills = ['python', 'c++']

    def check_role(self):
        if self.experience < self.expected_experience:
            self.reasons.append('Not enough experience')

        is_include = False
        for company in self._get_last_companies(2):
            if company.company_name.lower() in self.expected_companies:
                is_include = True
                break

        if not is_include:
            self.reasons.append('Not working in FAANG')

        is_include = True
        for company in self._get_last_companies(3):
            if company.job_title.lower() not in self.expected_roles:
                is_include = False
                break

        if not is_include:
            self.reasons.append('Job title does not match')

        is_include = True
        for skill in self.expected_skills:
            skills = [item.lower() for item in self._get_last_companies(1)[0].skills]
            if skill not in skills:
                is_include = False
                break

        if not is_include:
            self.reasons.append('Skills does not match')

        is_include = False
        if self.expected_city.lower() == self.profile.location.city.lower():
            is_include = True

        if not is_include:
            self.reasons.append('Applicant does not live in London')

        self._print_results()
