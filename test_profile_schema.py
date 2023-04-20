import datetime
import unittest

import pydantic

from profile_schema import Profile


class TestProfileSchemaExperiencesOrder(unittest.TestCase):
    def test_validation_error(self):
        profile_no_experiences = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": "abc"
        }
        self.assertRaises(
            pydantic.ValidationError,
            lambda: pydantic.parse_obj_as(Profile, profile_no_experiences)
        )

        profile_bad_experience = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": [
                {
                    "job_title": "", "description": "", "skills": [],
                    "starts_at": "2020-01-01",
                    "ends_at": "2023-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2017-01-01",
                    "ends_at": "2020-01-01",
                    "location": {"city": "", "country": ""}
                },
            ]
        }
        self.assertRaises(
            pydantic.ValidationError,
            lambda: pydantic.parse_obj_as(Profile, profile_bad_experience)
        )

    def test_preservces_empty_experiences(self):
        profile_empty_experiences = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": []
        }
        self.assertEqual(
            pydantic.parse_obj_as(Profile, profile_empty_experiences).experiences,
            []
        )

    def test_preserves_correct_experiences_order(self):
        profile_description = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": [
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2020-01-01",
                    "ends_at": "2023-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2017-01-01",
                    "ends_at": "2020-01-01",
                    "location": {"city": "", "country": ""}
                },
            ]
        }
        experiences = pydantic.parse_obj_as(Profile, profile_description).experiences
        self.assertEqual(
            (experiences[0].starts_at, experiences[0].ends_at),
            (datetime.date(2020, 1, 1), datetime.date(2023, 1, 1))
        )
        self.assertEqual(
            (experiences[1].starts_at, experiences[1].ends_at),
            (datetime.date(2017, 1, 1), datetime.date(2020, 1, 1))
        )

    def test_sorts_completed_experiences(self):
        profile_description = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": [
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2017-01-01",
                    "ends_at": "2020-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2020-01-01",
                    "ends_at": "2023-01-01",
                    "location": {"city": "", "country": ""}
                },
            ]
        }
        experiences = pydantic.parse_obj_as(Profile, profile_description).experiences
        self.assertEqual(
            (experiences[0].starts_at, experiences[0].ends_at),
            (datetime.date(2020, 1, 1), datetime.date(2023, 1, 1))
        )
        self.assertEqual(
            (experiences[1].starts_at, experiences[1].ends_at),
            (datetime.date(2017, 1, 1), datetime.date(2020, 1, 1))
        )

    def test_sorts_incompleted_experiences(self):
        profile_description = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": [
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2017-01-01",
                    "ends_at": "2020-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2020-01-01",
                    "location": {"city": "", "country": ""}
                },
            ]
        }
        experiences = pydantic.parse_obj_as(Profile, profile_description).experiences
        self.assertEqual(
            (experiences[0].starts_at, experiences[0].ends_at),
            (datetime.date(2020, 1, 1), None)
        )
        self.assertEqual(
            (experiences[1].starts_at, experiences[1].ends_at),
            (datetime.date(2017, 1, 1), datetime.date(2020, 1, 1))
        )

    def test_sorts_simultaneous_incompleted_experiences(self):
        profile_description = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": [
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2017-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2020-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2022-01-01",
                    "location": {"city": "", "country": ""}
                },
            ]
        }
        experiences = pydantic.parse_obj_as(Profile, profile_description).experiences
        self.assertEqual(
            (experiences[0].starts_at, experiences[0].ends_at),
            (datetime.date(2022, 1, 1), None)
        )
        self.assertEqual(
            (experiences[1].starts_at, experiences[1].ends_at),
            (datetime.date(2020, 1, 1), None)
        )
        self.assertEqual(
            (experiences[2].starts_at, experiences[2].ends_at),
            (datetime.date(2017, 1, 1), None)
        )

    def test_sorts_simultaneous_experiences(self):
        profile_description = {
            "first_name": "", "last_name": "", "description": "", "skills": [],
            "location": {"city": "", "country": ""},
            "experiences": [
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2017-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2022-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2020-01-01",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2016-01-01",
                    "ends_at": "2021-01-02",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2015-01-01",
                    "ends_at": "2016-01-02",
                    "location": {"city": "", "country": ""}
                },
                {
                    "company_name": "", "job_title": "", "description": "", "skills": [],
                    "starts_at": "2018-01-01",
                    "ends_at": "2019-01-02",
                    "location": {"city": "", "country": ""}
                },
            ]
        }
        experiences = pydantic.parse_obj_as(Profile, profile_description).experiences
        self.assertEqual(
            (experiences[0].starts_at, experiences[0].ends_at),
            (datetime.date(2022, 1, 1), None)
        )
        self.assertEqual(
            (experiences[1].starts_at, experiences[1].ends_at),
            (datetime.date(2020, 1, 1), None)
        )
        self.assertEqual(
            (experiences[2].starts_at, experiences[2].ends_at),
            (datetime.date(2017, 1, 1), None)
        )
        self.assertEqual(
            (experiences[3].starts_at, experiences[3].ends_at),
            (datetime.date(2016, 1, 1), datetime.date(2021, 1, 2))
        )
        self.assertEqual(
            (experiences[4].starts_at, experiences[4].ends_at),
            (datetime.date(2018, 1, 1), datetime.date(2019, 1, 2))
        )
        self.assertEqual(
            (experiences[5].starts_at, experiences[5].ends_at),
            (datetime.date(2015, 1, 1), datetime.date(2016, 1, 2))
        )


if __name__ == '__main__':
    unittest.main()
