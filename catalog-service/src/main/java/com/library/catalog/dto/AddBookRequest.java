package com.library.catalog.dto;

import jakarta.validation.constraints.NotNull;

public class AddBookRequest {

    @NotNull(message = "Book ID is required")
    private Long bookId;

    private String notes;

    public AddBookRequest() {}

    public AddBookRequest(Long bookId, String notes) {
        this.bookId = bookId;
        this.notes = notes;
    }

    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Long bookId;
        private String notes;

        public Builder bookId(Long bookId) { this.bookId = bookId; return this; }
        public Builder notes(String notes) { this.notes = notes; return this; }
        public AddBookRequest build() { return new AddBookRequest(bookId, notes); }
    }
}
