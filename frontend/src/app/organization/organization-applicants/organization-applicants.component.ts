import { Component } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { Profile } from 'src/app/models.module';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Organization } from '../organization.model';
import { organizationDetailResolver } from '../organization.resolver';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return (
    'Pending Applicants for ' + route.parent!.data['organization']?.name ??
    'Organization Not Found'
  );
};

@Component({
  selector: 'app-organization-applicants',
  templateUrl: './organization-applicants.component.html',
  styleUrls: ['./organization-applicants.component.css']
})
export class OrganizationApplicantsComponent {
  public static Route = {
    path: ':slug/applicants',
    title: 'Pending Applicants',
    component: OrganizationApplicantsComponent,
    resolve: {
      profile: profileResolver,
      organization: organizationDetailResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: OrganizationApplicantsComponent
      }
    ]
  };

  public profile: Profile;
  public organization: Organization;

  constructor(private route: ActivatedRoute) {
    const data = this.route.snapshot.data as {
      profile: Profile;
      organization: Organization;
    };
    this.profile = data.profile;
    this.organization = data.organization;
  }
}
