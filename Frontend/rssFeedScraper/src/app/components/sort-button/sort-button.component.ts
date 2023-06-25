import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-sort-button',
  template: `
    <button class="btn btn-outline-warning" (click)="toggleSort()">
      Sorting by {{ sortButtonLabel }}
    </button>
  `,
})
export class SortButtonComponent {
  changeSortingOrder: boolean = true;
  sortButtonLabel: string = 'Newest';

  @Output() sort = new EventEmitter<boolean>();

  toggleSort() {
    this.changeSortingOrder = !this.changeSortingOrder;

    //update the sort button label
    this.sortButtonLabel = this.changeSortingOrder ? 'Newest' : 'Oldest';

    this.sort.emit(this.changeSortingOrder);
  }
}
