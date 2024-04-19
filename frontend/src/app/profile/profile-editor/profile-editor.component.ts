import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { profileResolver } from '../profile.resolver';
import { Profile, ProfileService } from '../profile.service';
import { CommunityAgreement } from 'src/app/shared/community-agreement/community-agreement.widget';
import { MatDialog } from '@angular/material/dialog';
import { Member } from 'src/app/organization/organization.model';
import { MemberService } from 'src/app/organization/member.service';

@Component({
  selector: 'app-profile-editor',
  templateUrl: './profile-editor.component.html',
  styleUrls: ['./profile-editor.component.css']
})
export class ProfileEditorComponent implements OnInit {
  public static Route: Route = {
    path: 'profile',
    component: ProfileEditorComponent,
    title: 'Profile',
    canActivate: [isAuthenticated],
    resolve: { profile: profileResolver }
  };

  public profile: Profile;
  public token: string;
  public showToken: boolean = false;
  public memberships!: Member[];
  public yearOptions = [
    'Freshman',
    'Sophomore',
    'Junior',
    'Senior',
    'Graduate'
  ];

  public profileForm = this.formBuilder.group({
    first_name: '',
    last_name: '',
    email: '',
    pronouns: ''
  });

  public memberForm = this.formBuilder.group({
    major: '',
    minor: '',
    year: '',
    bio: ''
  });

  // TODO: Find better way to do this
  // Maybe have a function in Member Service to query it???
  terms: string[] = ['Spring 2024', 'Fall 2023', 'Spring 2023'];

  // Default to current term
  selectedTerm: string = MemberService.getCurrentTerm();

  constructor(
    route: ActivatedRoute,
    protected formBuilder: FormBuilder,
    protected profileService: ProfileService,
    protected snackBar: MatSnackBar,
    protected dialog: MatDialog,
    private memberService: MemberService
  ) {
    const form = this.profileForm;
    form.get('first_name')?.addValidators(Validators.required);
    form.get('lastname')?.addValidators(Validators.required);
    form
      .get('email')
      ?.addValidators([
        Validators.required,
        Validators.email,
        Validators.pattern(/unc\.edu$/)
      ]);
    form.get('pronouns')?.addValidators(Validators.required);

    const data = route.snapshot.data as { profile: Profile };
    this.profile = data.profile;

    this.token = `${localStorage.getItem('bearerToken')}`;
  }

  ngOnInit(): void {
    let profile = this.profile;

    this.loadMemberships();

    this.profileForm.setValue({
      first_name: profile.first_name,
      last_name: profile.last_name,
      email: profile.email,
      pronouns: profile.pronouns
    });
  }

  loadMemberships() {
    this.memberService
      .getUserMembershipsByTerm(this.profile.id!, this.selectedTerm)
      .subscribe((memberships) => {
        this.memberships = memberships;
        this.memberForm.setValue({
          major: this.memberships[0].major,
          minor: this.memberships[0].minor,
          year: this.memberships[0].year,
          bio: this.memberships[0].description
        });
      });
  }

  displayToken(): void {
    this.showToken = !this.showToken;
  }

  copyToken(): void {
    navigator.clipboard.writeText(this.token);
    this.snackBar.open('Token Copied', '', { duration: 2000 });
  }

  onSubmit(): void {
    if (this.profileForm.valid) {
      Object.assign(this.profile, this.profileForm.value);
      if (!this.profile.accepted_community_agreement) {
        const dialogRef = this.dialog.open(CommunityAgreement, {
          disableClose: true,
          autoFocus: 'dialog'
        });
        dialogRef.afterClosed().subscribe((profile) => {
          this.profile.accepted_community_agreement = true;
        });
      }
      this.profileService.put(this.profile).subscribe({
        next: (user) => this.onSuccess(user),
        error: (err) => this.onError(err)
      });
    }
  }

  submitOrganizationProfile(): void {
    if (this.memberForm.valid) {
      const formValues = this.memberForm.value;

      this.memberships.forEach((member) => {
        const updatedData = {
          major: formValues.major!,
          minor: formValues.minor!,
          year: formValues.year!,
          description: formValues.bio!
        };

        const updatedMember = { ...member, ...updatedData };

        this.memberService.updateMember(updatedMember).subscribe({
          next: () => {
            this.snackBar.open(
              'Organization Roster Profile Successfully Updated',
              '',
              {
                duration: 2000
              }
            );
          }
        });
      });
    }
  }

  private onSuccess(profile: Profile) {
    this.snackBar.open('Profile Saved', '', { duration: 2000 });
  }

  private onError(err: any) {
    console.error('How to handle this?');
  }

  linkWithGitHub(): void {
    this.profileService.getGitHubOAuthLoginURL().subscribe((url) => {
      window.location.href = url;
    });
  }

  unlinkGitHub() {
    this.profileService.unlinkGitHub().subscribe({
      next: () => (this.profile.github = '')
    });
  }

  openAgreementDialog(): void {
    const dialogRef = this.dialog.open(CommunityAgreement, {
      autoFocus: 'dialog'
    });
    this.profileService.profile$.subscribe();
    dialogRef.afterClosed().subscribe();
  }
}
