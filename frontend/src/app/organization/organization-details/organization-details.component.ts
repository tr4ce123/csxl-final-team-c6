/**
 * The Organization Detail Component displays more information and options regarding
 * UNC CS organizations.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn,
  Route,
  Router
} from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from '/workspace/frontend/src/app/profile/profile.resolver';
import { Member, Organization } from '../organization.model';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';
import {
  organizationDetailResolver,
  organizationEventsResolver,
  organizationMemberOnlyEventsResolver,
  organizationMembersResolver
} from '../organization.resolver';
import { EventService } from 'src/app/event/event.service';
import { Event } from 'src/app/event/event.model';
import { Observable } from 'rxjs';
import { PermissionService } from 'src/app/permission.service';
import { MemberService } from '../member.service';

/** Injects the organization's name to adjust the title. */
let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return route.parent!.data['organization']?.name ?? 'Organization Not Found';
};

@Component({
  selector: 'app-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css']
})
export class OrganizationDetailsComponent {
  /** Route information to be used in Organization Routing Module */
  public static Route: Route = {
    path: ':slug',
    component: OrganizationDetailsComponent,
    resolve: {
      profile: profileResolver,
      organization: organizationDetailResolver,
      events: organizationEventsResolver,
      members: organizationMembersResolver,
      memberOnlyEvents: organizationMemberOnlyEventsResolver
    },
    children: [
      {
        path: '',
        title: titleResolver,
        component: OrganizationDetailsComponent
      }
    ]
  };

  /** Store the currently-logged-in user's profile.  */
  public profile: Profile;

  /** The organization to show */
  public organization: Organization;

  /** Store a map of days to a list of events for that day */
  public eventsPerDay: [string, Event[]][];

  public memberOnlyEventsPerDay: [string, Event[]][];

  /** Whether or not the user has permission to update events. */
  public eventCreationPermission$: Observable<boolean>;

  /** The leaders of the organization to show */
  public leaders: Member[];

  public isMember: boolean = false;

  /** Constructs the Organization Detail component */
  constructor(
    private route: ActivatedRoute,
    protected snackBar: MatSnackBar,
    protected eventService: EventService,
    private permission: PermissionService,
    protected router: Router,
    protected memberService: MemberService
  ) {
    /** Initialize data from resolvers. */
    const data = this.route.snapshot.data as {
      profile: Profile;
      organization: Organization;
      events: Event[];
      memberOnlyEvents: Event[];
      members: Member[];
    };
    this.profile = data.profile;
    this.organization = data.organization;
    this.eventsPerDay = eventService.groupEventsByDate(data.events ?? []);
    this.memberOnlyEventsPerDay = eventService.groupEventsByDate(
      data.memberOnlyEvents ?? []
    );
    this.eventCreationPermission$ = this.permission.check(
      'organization.events.*',
      `organization/${this.organization?.id ?? -1}`
    );
    this.leaders = this.getLeadersFromAllMembers(data.members);
    this.checkMembership();
  }

  private getLeadersFromAllMembers(members: Member[]): Member[] {
    let leaders: Member[] = members.filter(
      (member) => member.position !== 'Member'
    );

    leaders.sort((a, b) => {
      if (a.position === 'President') {
        return -1;
      } else if (b.position === 'President') {
        return 1;
      } else if (
        a.position === 'Vice President' &&
        b.position !== 'President'
      ) {
        return -1;
      } else if (
        b.position === 'Vice President' &&
        a.position !== 'President'
      ) {
        return 1;
      }
      return 0;
    });

    return leaders;
  }

  checkMembership() {
    this.memberService
      .getMembersByOrgAndUser(this.organization?.slug!, this.profile?.id!)
      .subscribe(() => {
        this.isMember = true;
      });
  }
}
