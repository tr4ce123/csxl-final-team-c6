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
import { Organization } from '../organization.model';
import { organizationDetailResolver } from '../organization.resolver';
import { OrganizationService } from '../organization.service';

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
  email = new FormControl('', [Validators.email]);
  major = new FormControl('', Validators.required);
  year = new FormControl(0, [Validators.required]);
  pronouns = new FormControl('', [Validators.required]);
  interest = new FormControl('', [Validators.required]);

  public applicationForm = this.formBuilder.group({
    name: this.name,
    email: this.email,
    major: this.major,
    year: this.year,
    pronouns: this.pronouns,
    interest: this.interest
  });

  isNew: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private snackBar: MatSnackBar,
    protected organizationService: OrganizationService
  ) {
    // determine applicant is new
    this.route.data.subscribe((data) => {
      if (data['profile']) {
        this.isNew = false;
      } else {
        this.isNew = true;
      }
    });
  }

  // when someone submits a form, send info into createForm function in service
  onSubmit() {
    if (this.applicationForm.valid) {
      if (this.isNew) {
        this.organizationService
          .createForm({
            name: this.name.value ?? '',
            email: this.email.value ?? '',
            major: this.major.value ?? '',
            year: this.year.value ?? 0,
            pronouns: this.pronouns.value ?? '',
            interest: this.interest.value ?? ''
          })
          .subscribe((_) => {
            this.router.navigate(['/organizations']);
          });
      }
    } else {
      this.snackBar.open('Please enter values in the form correctly.', '', {
        duration: 2000
      });
    }
  }
}
