import { Component } from '@angular/core';
import { FormBuilder, FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Router
} from '@angular/router';
import { Profile } from 'src/app/models.module';
import { profileResolver } from 'src/app/profile/profile.resolver';
import {
  Applicant,
  ApplicantStatus,
  Organization
} from '../organization.model';
import { organizationDetailResolver } from '../organization.resolver';
import { OrganizationService } from '../organization.service';
import { ApplicantService } from '../applicant.service';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return (
    'Application for ' + route.parent!.data['organization']?.name ??
    'Organization Not Found'
  );
};

@Component({
  selector: 'app-organization-application',
  templateUrl: './organization-application.component.html',
  styleUrls: ['./organization-application.component.css']
})
export class OrganizationApplicationComponent {
  public static Route = {
    path: ':slug/application',
    title: 'Application Form',
    component: OrganizationApplicationComponent,
    resolve: {
      profile: profileResolver,
      organization: organizationDetailResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: OrganizationApplicationComponent
      }
    ]
  };

  name = new FormControl('', [Validators.required]);
  email = new FormControl('', [Validators.email, Validators.required]);
  major = new FormControl('', Validators.required);
  minor = new FormControl('');
  year = new FormControl('', [Validators.required]);
  pronouns = new FormControl('', [Validators.required]);
  interest = new FormControl('', [Validators.required]);

  public applicationForm = this.formBuilder.group({
    name: this.name,
    email: this.email,
    major: this.major,
    minor: this.minor,
    year: this.year,
    pronouns: this.pronouns,
    interest: this.interest
  });

  /** Store the organization.  */
  public organization: Organization;

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile | null = null;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar,
    private organizationService: OrganizationService,
    private applicantService: ApplicantService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      organization: Organization;
    };
    this.profile = data.profile;
    this.organization = data.organization;
  }

  // when someone submits a form, send info into createForm function in service
  onSubmit() {
    if (this.applicationForm.valid) {
      const newApplicant: Applicant = {
        id: 0, // Value does not matter
        user_id: this.profile!.id!,
        organization_id: this.organization.id!,
        status: ApplicantStatus.Pending,
        name: this.applicationForm.value.name!,
        email: this.applicationForm.value.email!,
        major: this.applicationForm.value.major!,
        minor: this.applicationForm.value.minor ?? null,
        year: this.applicationForm.value.year!,
        pronouns: this.applicationForm.value.pronouns!,
        interest: this.applicationForm.value.interest!
      };
      console.log('Past new applicant');
      this.applicantService
        .createApplicant(this.organization.slug, newApplicant)
        .subscribe({
          next: (applicant) => {
            this.router.navigate(['/organizations/' + this.organization?.slug]);
            this.snackBar.open(
              'You have successfully applied to ' + this.organization?.name,
              '',
              {
                duration: 2000
              }
            );
          },
          error: (error) => {
            console.error('Failed to create applicant:', error);
            this.snackBar.open('Failed to submit application.', '', {
              duration: 2000
            });
          }
        });
    } else {
      this.snackBar.open('Please enter values in the form correctly.', '', {
        duration: 2000
      });
    }
  }
}
