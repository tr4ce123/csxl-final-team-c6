/**
 * The Organization Details Info Card widget abstracts the implementation of each
 * individual organization detail card from the whole organization detail page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Subscription } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  ApplicantStatus,
  Organization,
  OrganizationType
} from '../../organization.model';
import { Profile } from 'src/app/profile/profile.service';
import { PermissionService } from 'src/app/permission.service';
import { Observable } from 'rxjs';
import { MemberService } from '../../member.service';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApplicantService } from '../../applicant.service';

@Component({
  selector: 'organization-details-info-card',
  templateUrl: './organization-details-info-card.widget.html',
  styleUrls: ['./organization-details-info-card.widget.css']
})
export class OrganizationDetailsInfoCard implements OnInit, OnDestroy {
  /** The organization to show */
  @Input() organization?: Organization;
  /** The currently logged in user */
  @Input() profile?: Profile;

  /** Holds data on whether or not the user is on a mobile device */
  public isHandset: boolean = false;
  private isHandsetSubscription!: Subscription;

  /** Holds data on whether or not the user is on a tablet */
  public isTablet: boolean = false;
  private isTabletSubscription!: Subscription;

  /** Holds data on whether or not the user is a member of the organization */
  public isMember: boolean = false;

  public appIsPending: boolean = false;

  public isLeader: boolean = false;

  organizationType = OrganizationType;

  applicantStatus = ApplicantStatus;

  // Default to current term
  selectedTerm: string = MemberService.getCurrentTerm();

  /** Constructs the organization detail info card widget */
  constructor(
    private breakpointObserver: BreakpointObserver,
    private route: ActivatedRoute,
    private permission: PermissionService,
    private memberService: MemberService,
    protected router: Router,
    protected snackBar: MatSnackBar,
    private applicantService: ApplicantService
  ) {}

  checkPermissions(): Observable<boolean> {
    return this.permission.check(
      'organization.update',
      `organization/${this.organization?.slug}`
    );
  }

  /** Runs whenever the view is rendered initally on the screen */
  ngOnInit(): void {
    this.isHandsetSubscription = this.initHandset();
    this.isTabletSubscription = this.initTablet();
    this.checkMembership();
    this.checkApplicationStatus();
  }

  /** Unsubscribe from subscribers when the page is destroyed */
  ngOnDestroy(): void {
    this.isHandsetSubscription.unsubscribe();
    this.isTabletSubscription.unsubscribe();
  }

  /** Determines whether the page is being used on a mobile device */
  private initHandset() {
    return this.breakpointObserver
      .observe([Breakpoints.Handset, Breakpoints.TabletPortrait])
      .pipe(map((result) => result.matches))
      .subscribe((isHandset) => (this.isHandset = isHandset));
  }

  /** Determines whether the page is being used on a tablet */
  private initTablet() {
    return this.breakpointObserver
      .observe(Breakpoints.TabletLandscape)
      .pipe(map((result) => result.matches))
      .subscribe((isTablet) => (this.isTablet = isTablet));
  }

  checkMembership() {
    this.memberService
      .getMembersByOrgAndUser(this.organization?.slug!, this.profile?.id!)
      .subscribe((member) => {
        this.isMember = true;
        this.isLeader = member.isLeader;
      });
  }

  checkApplicationStatus() {
    this.applicantService
      .getApplicants(this.organization?.slug!)
      .subscribe((applicants) => {
        this.appIsPending = applicants.some(
          (applicant) =>
            applicant.user_id == this.profile?.id &&
            applicant.status == this.applicantStatus.Pending
        );
      });
  }

  leaveOrganization() {
    if (this.isMember) {
      let confirmLeave = this.snackBar.open(
        'Are you sure you want to leave this organization?',
        'Leave',
        { duration: 15000 }
      );

      confirmLeave.onAction().subscribe(() => {
        this.memberService
          .deleteMember(
            this.organization?.slug!,
            this.profile?.id!,
            this.selectedTerm
          )
          .subscribe(() => {
            this.snackBar.open('You left ' + this.organization?.name, '', {
              duration: 2000
            });
            this.isMember = false;
            this.isLeader = false;
          });
      });
    }
  }

  joinOrganization() {
    if (this.organization?.org_type == this.organizationType.OPEN) {
      this.memberService
        .joinOrganizationWithExistingDetails(
          this.organization.slug,
          this.profile?.id!,
          this.selectedTerm
        )
        .subscribe({
          next: () => {
            this.isMember = true;
            this.snackBar.open('You joined ' + this.organization?.name, '', {
              duration: 2000
            });
          }
        });
    }
  }

  viewPendingApplications() {
    this.router.navigate(['applicants'], { relativeTo: this.route });
  }
}
function subscribe(arg0: (member: any) => void) {
  throw new Error('Function not implemented.');
}
