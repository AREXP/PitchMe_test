from applicants.base import BaseApplicant
from constants import EU_COUNTRIES
from profile_schema import Profile


class MiddleUXDesigner(BaseApplicant):

    def __init__(self, profile: Profile) -> None:
        super().__init__(profile)
        self.expected_roles = ['product designer', 'ux-designer']
        self.expected_skills = ['figma', 'sketch', 'ux-research', 'miro']

    def check_role(self):
        is_include = False
        for company in self._get_last_companies(2):
            if company.job_title.lower() in self.expected_roles:
                is_include = True
                break

        if not is_include:
            self.reasons.append('Role does not match')

        include_count = 0
        for skill in self.profile.skills:
            if skill.lower() in self.expected_skills:
                include_count += 1

        if include_count < 2:
            self.reasons.append('Skills does not match')

        if self.last_experience < 2:
            self.reasons.append('Last experience does not match')

        if self.experience > 5:
            self.reasons.append('Experience more then 5 years')

        if self.profile.location.country.lower() not in EU_COUNTRIES:
            self.reasons.append('Applicant does not live in EU')

        self._print_results()
