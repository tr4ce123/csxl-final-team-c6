import { Component } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route,
  Router
} from '@angular/router';
import { Profile } from 'src/app/models.module';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { Organization } from '../organization.model';
import { organizationDetailResolver } from '../organization.resolver';
import { OrganizationService } from '../organization.service';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return (
    'Members of ' + route.parent!.data['organization']?.name ??
    'Organization Not Found'
  );
};

@Component({
  selector: 'app-organization-roster',
  templateUrl: './organization-roster.component.html',
  styleUrls: ['./organization-roster.component.css']
})
export class OrganizationRosterComponent {
  public static Route: Route = {
    path: ':slug/roster',
    title: 'Organization Roster',
    component: OrganizationRosterComponent,
    resolve: {
      profile: profileResolver,
      organization: organizationDetailResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: OrganizationRosterComponent
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
