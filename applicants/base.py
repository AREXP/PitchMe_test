from datetime import date, timedelta
from typing import List

from profile_schema import Profile, Experience


class BaseApplicant:

    def __init__(self, profile: Profile) -> None:
        self.profile = profile
        self.experience = self._get_experience()
        self.companies: List[Experience] = self._get_companies()
        self.reasons = []

    def check_role(self):
        raise NotImplemented('Method not implemented')

    def _get_companies(self) -> List[Experience]:
        return [item for item in self.profile.experiences]

    def _get_experience(self):
        tmp = []
        for experience in self.profile.experiences:
            if not experience.ends_at:
                experience.ends_at = date.today()
            if not tmp:
                tmp.append([experience.starts_at, experience.ends_at])
                continue

            copy_tmp = tmp.copy()
            for dates in copy_tmp:
                is_change = False
                if experience.starts_at > dates[0] and experience.ends_at < dates[1]:
                    continue
                if experience.starts_at < dates[0] and experience.ends_at > dates[1]:
                    dates[0] = experience.starts_at
                    dates[1] = experience.ends_at
                    continue
                if experience.starts_at <= dates[0] <= experience.ends_at <= dates[1]:
                    is_change = True
                    dates[0] = experience.starts_at
                if dates[0] <= experience.starts_at <= dates[1] <= experience.ends_at:
                    is_change = True
                    dates[1] = experience.ends_at

                if not is_change:
                    tmp.append([experience.starts_at, experience.ends_at])

        result = timedelta(0)
        for dates in tmp:
            diff = dates[1] - dates[0]
            result += diff

        return round(result.days/365, 2)

    @property
    def last_experience(self) -> float:
        company = self._get_last_companies(1)[0]
        return round((company.ends_at - company.starts_at).days/365, 2)

    def _get_last_companies(self, count=1) -> List[Experience]:
        count = len(self.companies) if count < len(self.companies) else count

        return sorted(self.companies, key=lambda x: x.ends_at, reverse=True)[:count]

    def _print_results(self):
        if self.reasons:
            print(f'{self.profile.full_name} - False, {self.reasons[0]}')
        else:
            print(f'{self.profile.full_name} - True')