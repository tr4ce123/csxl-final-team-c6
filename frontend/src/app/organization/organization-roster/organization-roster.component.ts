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
import { Member, Organization, MemberYear } from '../organization.model';
import {
  organizationDetailResolver,
  organizationMembersResolver
} from '../organization.resolver';
import { MemberService } from '../member.service';
import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return (
    'Members of ' + route.parent!.data['organization']?.name ??
    'Organization Not Found'
  );
};

@Component({
  selector: 'app-organization-roster',
  templateUrl: './organization-roster.component.html',
  styleUrls: ['./organization-roster.component.css'],
  animations: [
    trigger('detailExpand', [
      state('collapsed,void', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      )
    ])
  ]
})
export class OrganizationRosterComponent {
  public static Route: Route = {
    path: ':slug/roster',
    title: 'Organization Roster',
    component: OrganizationRosterComponent,
    resolve: {
      profile: profileResolver,
      organization: organizationDetailResolver,
      members: organizationMembersResolver
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

  public members: Member[];

  public memberYear = MemberYear;

  /** Store the columns to display in the table */
  public displayedColumns: string[] = ['name', 'role'];
  /** Store the columns to display when extended */
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  /** Store the element where the dropdown is currently active */
  public expandedElement!: Member;

  constructor(
    private route: ActivatedRoute,
    public memberService: MemberService
  ) {
    const data = this.route.snapshot.data as {
      profile: Profile;
      organization: Organization;
      members: Member[];
    };
    this.profile = data.profile;
    this.organization = data.organization;
    this.members = data.members;
  }
}
