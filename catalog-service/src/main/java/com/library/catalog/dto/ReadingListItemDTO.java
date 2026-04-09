package com.library.catalog.dto;

import java.time.LocalDate;

public class ReadingListItemDTO {
    private Long id;
    private Long bookId;
    private String bookTitle;
    private String bookAuthor;
    private LocalDate addedDate;
    private String notes;
    private String readStatus;

    public ReadingListItemDTO() {}

    public ReadingListItemDTO(Long id, Long bookId, String bookTitle, String bookAuthor, LocalDate addedDate, String notes, String readStatus) {
        this.id = id;
        this.bookId = bookId;
        this.bookTitle = bookTitle;
        this.bookAuthor = bookAuthor;
        this.addedDate = addedDate;
        this.notes = notes;
        this.readStatus = readStatus;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
    public String getBookTitle() { return bookTitle; }
    public void setBookTitle(String bookTitle) { this.bookTitle = bookTitle; }
    public String getBookAuthor() { return bookAuthor; }
    public void setBookAuthor(String bookAuthor) { this.bookAuthor = bookAuthor; }
    public LocalDate getAddedDate() { return addedDate; }
    public void setAddedDate(LocalDate addedDate) { this.addedDate = addedDate; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public String getReadStatus() { return readStatus; }
    public void setReadStatus(String readStatus) { this.readStatus = readStatus; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Long id;
        private Long bookId;
        private String bookTitle;
        private String bookAuthor;
        private LocalDate addedDate;
        private String notes;
        private String readStatus;

        public Builder id(Long id) { this.id = id; return this; }
        public Builder bookId(Long bookId) { this.bookId = bookId; return this; }
        public Builder bookTitle(String bookTitle) { this.bookTitle = bookTitle; return this; }
        public Builder bookAuthor(String bookAuthor) { this.bookAuthor = bookAuthor; return this; }
        public Builder addedDate(LocalDate addedDate) { this.addedDate = addedDate; return this; }
        public Builder notes(String notes) { this.notes = notes; return this; }
        public Builder readStatus(String readStatus) { this.readStatus = readStatus; return this; }
        public ReadingListItemDTO build() { return new ReadingListItemDTO(id, bookId, bookTitle, bookAuthor, addedDate, notes, readStatus); }
    }
}
