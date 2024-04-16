/**
 * The Organization Card widget abstracts the implementation of each
 * individual organization card from the whole organization page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2023
 * @license MIT
 */

import { Component, Input } from '@angular/core';
import { Organization, OrganizationType } from '../../organization.model';
import { Profile } from '/workspace/frontend/src/app/profile/profile.service';

@Component({
  selector: 'organization-card',
  templateUrl: './organization-card.widget.html',
  styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {
  /** The organization to show */
  @Input() organization!: Organization;
  /** The profile of the currently signed in user */
  @Input() profile?: Profile;
  /** @deprecated Stores the permission values for a profile */
  @Input() profilePermissions!: Map<number, number>;

  organizationType = OrganizationType;

  getTooltipMessage(orgType: OrganizationType): string {
    switch (orgType) {
      case OrganizationType.OPEN:
        return 'Open';
      case OrganizationType.APP:
        return 'Application Only';
      case OrganizationType.CLOSED:
        return 'Closed';
      default:
        return '';
    }
  }

  /**
   * Determines whether or not the tooltip on the card is disabled
   * @param element: The HTML element
   * @returns {boolean}
   */
  isTooltipDisabled(element: HTMLElement): boolean {
    return element.scrollHeight <= element.clientHeight;
  }

  constructor() {}
}
