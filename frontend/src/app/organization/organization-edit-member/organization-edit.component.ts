import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { MemberService } from '../member.service';
import { Member, Organization } from '../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { profileResolver } from 'src/app/profile/profile.resolver';
import {
  organizationDetailResolver,
  organizationMemberDetailResolver
} from '../organization.resolver';
import { Profile } from 'src/app/models.module';

@Component({
  selector: 'app-organization-edit',
  templateUrl: './organization-edit-member.component.html',
  styleUrls: ['./organization-edit-member.component.css']
})
export class OrganizationEditMemberComponent {
  public static Route = {
    path: ':slug/edit/:id',
    title: 'Edit Member',
    component: OrganizationEditMemberComponent,
    resolve: {
      profile: profileResolver,
      organization: organizationDetailResolver,
      member: organizationMemberDetailResolver
    }
  };

  public organization: Organization;
  public member: Member;
  public memberId: number;
  public profile: Profile;

  selectedTerm: string = MemberService.getCurrentTerm();

  constructor(
    private route: ActivatedRoute,
    protected router: Router,
    private memberService: MemberService,
    private snackBar: MatSnackBar
  ) {
    const data = this.route.snapshot.data as {
      organization: Organization;
      member: Member;
      profile: Profile;
    };
    this.organization = data.organization;
    this.member = data.member;
    this.profile = data.profile;

    let memberId = this.route.snapshot.params['id'];
    this.memberId = memberId;
  }

  toggleLeader() {
    this.member.isLeader = !this.member.isLeader;
    this.memberService.updateMember(this.member).subscribe({
      next: () => {
        if (this.member.isLeader) {
          this.snackBar.open(
            'You granted ' +
              this.member.user.first_name +
              ' leadership permissions.',
            '',
            {
              duration: 2000
            }
          );
        } else {
          this.snackBar.open(
            'You revoked ' +
              this.member.user.first_name +
              "'s leadership permissions.",
            '',
            {
              duration: 2000
            }
          );
        }
      },
      error: (err) => {
        console.error('Failed to make member a leader:', err);
        this.snackBar.open(
          'Error granting leadership. Please try again.',
          'Close',
          { duration: 2000 }
        );
      }
    });
  }

  updatePosition() {
    this.memberService.updateMember(this.member).subscribe({
      next: () => {
        this.snackBar.open('Position updated successfully!', '', {
          duration: 2000
        });
      },
      error: () => {
        this.snackBar.open(
          'Error updating position. Please try again.',
          'Close',
          {
            duration: 2000
          }
        );
      }
    });
  }

  removeMember() {
    this.memberService
      .deleteMember(
        this.organization.slug,
        this.member!.user_id,
        this.selectedTerm
      )
      .subscribe({
        next: () => {
          this.router.navigate([
            `organizations/${this.organization.slug}/roster`
          ]);
          this.snackBar.open('Member removed successfully', 'Close', {
            duration: 3000
          });
        },
        error: (error) => {
          console.error('Error removing member:', error);
          this.snackBar.open('Failed to remove member', 'Close', {
            duration: 3000
          });
        }
      });
  }
}
