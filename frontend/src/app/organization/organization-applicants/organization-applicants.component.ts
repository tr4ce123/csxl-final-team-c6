import { Component, OnInit } from '@angular/core';
import {
  ActivatedRoute,
  ActivatedRouteSnapshot,
  ResolveFn
} from '@angular/router';
import { Profile } from 'src/app/models.module';
import { profileResolver } from 'src/app/profile/profile.resolver';
import {
  Applicant,
  ApplicantStatus,
  Organization
} from '../organization.model';
import { organizationDetailResolver } from '../organization.resolver';
import { ApplicantService } from '../applicant.service';
import { MemberService } from '../member.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import {
  animate,
  state,
  style,
  transition,
  trigger
} from '@angular/animations';

let titleResolver: ResolveFn<string> = (route: ActivatedRouteSnapshot) => {
  return (
    'Pending Applicants for ' + route.parent!.data['organization']?.name ??
    'Organization Not Found'
  );
};

@Component({
  selector: 'app-organization-applicants',
  templateUrl: './organization-applicants.component.html',
  styleUrls: ['./organization-applicants.component.css'],
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
export class OrganizationApplicantsComponent implements OnInit {
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
  public applicants!: Applicant[];

  // TODO: Find better way to do this
  // Maybe have a function in Member Service to query it???
  terms: string[] = ['Spring 2024', 'Fall 2023', 'Spring 2023'];

  // Default to current term
  selectedTerm: string = MemberService.getCurrentTerm();

  public displayedColumns: string[] = ['name', 'major', 'year'];
  /** Store the columns to display when extended */
  public columnsToDisplayWithExpand = [...this.displayedColumns, 'expand'];
  /** Store the element where the dropdown is currently active */
  public expandedElement!: Applicant;

  constructor(
    private route: ActivatedRoute,
    private applicantService: ApplicantService,
    private memberService: MemberService,
    protected snackBar: MatSnackBar
  ) {
    const data = this.route.snapshot.data as {
      profile: Profile;
      organization: Organization;
    };
    this.profile = data.profile;
    this.organization = data.organization;
  }
  ngOnInit(): void {
    this.loadApplicants();
  }

  loadApplicants() {
    this.applicantService
      .getApplicants(this.organization.slug)
      .subscribe((applicants) => {
        this.applicants = applicants;
      });
  }

  accept(applicant: Applicant) {
    // Update status field
    applicant.status = ApplicantStatus.Accepted;

    // Update the application to be accepted
    this.applicantService
      .updateApplicant(applicant.id, applicant)
      .subscribe(() => {
        this.loadApplicants();
      });

    // Add new member to the organization
    this.memberService
      .joinOrganizationWithExistingDetails(
        this.organization.slug,
        applicant.user_id,
        this.selectedTerm
      )
      .subscribe({
        next: () => {
          this.snackBar.open(
            'You accepted ' + applicant.name + ' into your organization',
            '',
            { duration: 2000 }
          );
        }
      });
  }

  reject(applicant: Applicant) {
    applicant.status = ApplicantStatus.Rejected;

    // Logic to reject the applicant
    console.log('Rejected:', applicant);

    // Update the application to be rejected
    this.applicantService
      .updateApplicant(applicant.id, applicant)
      .subscribe((result) => {
        this.loadApplicants();
      });
  }
}
