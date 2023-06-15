import { Component, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-sort-button',
  template: `
    <button class="btn btn-outline-primary" (click)="toggleSort()">
      {{ sortButtonLabel }}
    </button>
  `
})
export class SortButtonComponent {
  changeSortingOrder: boolean = true;
  sortButtonLabel: string = 'A->Z';

  @Output() sort = new EventEmitter<boolean>();

  toggleSort() {
    this.changeSortingOrder = !this.changeSortingOrder;
    
    //update the sort button label
    this.sortButtonLabel = this.changeSortingOrder ? 'A->Z' : 'Z->A';

    this.sort.emit(this.changeSortingOrder);
  }
}
