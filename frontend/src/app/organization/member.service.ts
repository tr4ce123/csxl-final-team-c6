import { Injectable } from '@angular/core';
import { AuthenticationService } from '../authentication.service';
import { HttpClient } from '@angular/common/http';
import { Observable, Subscription, switchMap } from 'rxjs';
import { Member } from './organization.model';
import { Profile, ProfileService } from '../profile/profile.service';

@Injectable({
  providedIn: 'root'
})
export class MemberService {
  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected profileSvc: ProfileService
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  static getCurrentTerm(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    let term: string;

    if (month >= 0 && month <= 5) {
      term = 'Spring';
    } else {
      term = 'Fall';
    }

    return `${term} ${year}`;
  }

  /** Get all member entries from the backend database table using the backend HTTP get request.
   * @returns {Observable<Member[]>}
   */
  getMembers(slug: string): Observable<Member[]> {
    return this.http.get<Member[]>('/api/members/' + slug);
  }

  /** Get a member by its ID using the backend HTTP get request.
   * @returns {Observable<Member>}
   */
  getMemberById(id: number): Observable<Member> {
    return this.http.get<Member>(`/api/members/id/id/${id}`);
  }

  /** Get all member entries for a given term from the backend database table using HTTP get request
   * @returns {Observable<Member[]>}
   */
  getMembersByTerm(slug: string, term: string): Observable<Member[]> {
    return this.http.get<Member[]>('/api/members/' + slug + '/' + term);
  }

  /** Get all member entries associated with a user from the backend database table using the backend HTTP get request.
   * @returns {Observable<Member[]>}
   */
  getUserMemberships(userId: number): Observable<Member[]> {
    return this.http.get<Member[]>(`/api/members/user/memberships/${userId}`);
  }

  /** Get all member entries associated with a user by term from the backend database table using the backend HTTP get request.
   * @returns {Observable<Member[]>}
   */
  getUserMembershipsByTerm(userId: number, term: string): Observable<Member[]> {
    return this.http.get<Member[]>(
      `/api/members/user/memberships/${userId}/${term}`
    );
  }

  /** Delete the given member object using the backend HTTP delete request.
   * @param slug: The organization to delete the member from
   * @returns void
   */
  deleteMember(slug: string, userId: number, term: string): Observable<any> {
    return this.http.delete(`/api/members/${slug}/delete/${userId}/${term}`);
  }

  /** Create a member object using the backend HTTP post request.
   * @param slug: The organization to add the member to
   * @returns void
   */
  addMember(slug: string, userId: number, term: string): Observable<Member> {
    return this.http.post<Member>(
      `/api/members/${slug}/create/${userId}/${term}`,
      {}
    );
  }

  /** Update a member object using the backend HTTP post request.
   * @param member: The organization to add the member to
   * @returns {Observable<Member>}
   */
  updateMember(member: Member): Observable<Member> {
    return this.http.put<Member>('/api/members', member);
  }

  /**
   * Joins an organization and applies existing member attributes if available.
   * @param slug: The organization to add the member to
   * @param userId: id of the member joining
   * @returns {Observable<Member>}
   */
  joinOrganizationWithExistingDetails(
    slug: string,
    userId: number,
    term: string
  ): Observable<Member> {
    return this.getUserMembershipsByTerm(userId, term).pipe(
      switchMap((existingMembers) => {
        if (existingMembers.length > 0) {
          const tempMember = existingMembers[0];
          return this.addMember(slug, userId, term).pipe(
            switchMap((newMember) => {
              newMember.major = tempMember.major;
              newMember.minor = tempMember.minor;
              newMember.description = tempMember.description;
              newMember.year = tempMember.year;
              return this.updateMember(newMember);
            })
          );
        } else {
          return this.addMember(slug, userId, term);
        }
      })
    );
  }
}
