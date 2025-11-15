import os
import time
import pytest
from datetime import datetime
from pages.home_page import HomePage
from pages.jobs_page import JobsPage
from pages.signup_page import SignUpPage

@pytest.mark.order(1)
def test_qajobs_signup_flow(driver):
    """
    Full signup flow:
      1) open site
      #2) go to QA Jobs
      3) Sign Up -> Candidate
      4) fill form
      5) tick ONLY the checkbox square
      6) click Register and report what happened (redirect / success / error)
      7) keep page visible for 10s (for manual observation)
    """
    # Where to save screenshots
    screenshots_dir = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # Initialize page objects
    home = HomePage(driver)
    jobs = JobsPage(driver)
    signup = SignUpPage(driver)

    try:
        # Step 1: Go to the homepage
        home.go_to_site()
        print("Navigating to homepage...")

        # Step 2: Click on the "QA Jobs" link
        home.click_qa_jobs()
        print("Clicked on 'QA Jobs' link.")

        # Step 3: Click on "Sign Up" and select the "Candidate" option from the dropdown
        jobs.click_sign_up()
        signup.select_candidate()
        print("Opened Candidate signup form.")

        # Step 4: Fill in the registration form
        signup.fill_registration_form(
            username="shad008",
            email="shad009@google.com",
            first_name="Shad",
            last_name="Ahmed"
        )
        print("Filled registration form fields.")

        # Step 5: Agree to the terms and conditions (click square only)
        signup.agree_to_terms_and_conditions()
        print("Clicked checkbox square (terms accepted).")

        # Step 6: Click "Register Now" and keep the page visible for 10s
        outcome = signup.click_register_link(stay_seconds=10)
        print(f"[TEST] Outcome after Register: {outcome}")

        # Optional soft assertion: outcome should report something meaningful
        assert isinstance(outcome, str) and len(outcome) > 0

    finally:
        # Always save a screenshot of the final state for debugging
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        shot_path = os.path.join(screenshots_dir, f"signup_outcome_{ts}.png")
        try:
            driver.save_screenshot(shot_path)
            print(f"[TEST] Screenshot saved to: {shot_path}")
        except Exception as e:
            print(f"[TEST] Failed to save screenshot: {e}")
