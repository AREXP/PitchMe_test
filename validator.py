from profile_schema import Profile


class Validator:
    @staticmethod
    def is_experienced_python_developer(profile: Profile) -> bool:
        # Conditions for an experienced Python developer
        last_two_jobs = profile.experiences[-2:]
        faang_worked = any("FAANG" in job.company_name for job in last_two_jobs)
        backend_or_software_engineer = any(
            job.job_title in ["Backend developer", "Software engineer"] for job in last_two_jobs
        )
        total_experience = len(set(exp.starts_at.year for exp in profile.experiences))
        python_and_cpp_skills = {"Python", "C++"}.issubset(profile.skills)
        lives_in_london = profile.location.city == "London"

        return faang_worked and backend_or_software_engineer and total_experience > 8 and python_and_cpp_skills and lives_in_london

    @staticmethod
    def is_middle_ux_designer(profile: Profile) -> bool:
        # Conditions for a middle UX designer
        last_two_jobs = profile.experiences[-2:]
        product_or_ux_designer = any(
            job.job_title in ["Product designer", "UX-designer"] for job in last_two_jobs
        )
        figma_sketch_ux_research_miro = {"Figma", "Sketch", "UX-research", "Miro"}.issubset(
            profile.skills
        )
        eu_location = profile.location.country == "European Union"
        last_employment_experience = profile.experiences[-1]
        more_than_two_years_experience = (
                last_employment_experience.ends_at.year - last_employment_experience.starts_at.year > 2
        )
        total_experience = len(set(exp.starts_at.year for exp in profile.experiences))
        less_than_five_years_experience = total_experience < 5

        return (
                product_or_ux_designer
                and figma_sketch_ux_research_miro
                and eu_location
                and more_than_two_years_experience
                and less_than_five_years_experience
        )
