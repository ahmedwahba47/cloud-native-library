package com.library.catalog.entity;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "reading_list_items")
public class ReadingListItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "book_id", nullable = false)
    private Long bookId;

    @Column(name = "added_date")
    private LocalDate addedDate;

    private String notes;

    @Column(name = "read_status")
    @Enumerated(EnumType.STRING)
    private ReadStatus readStatus = ReadStatus.TO_READ;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reading_list_id", nullable = false)
    private ReadingList readingList;

    public ReadingListItem() {}

    public ReadingListItem(Long id, Long bookId, LocalDate addedDate, String notes, ReadStatus readStatus, ReadingList readingList) {
        this.id = id;
        this.bookId = bookId;
        this.addedDate = addedDate;
        this.notes = notes;
        this.readStatus = readStatus != null ? readStatus : ReadStatus.TO_READ;
        this.readingList = readingList;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getBookId() { return bookId; }
    public void setBookId(Long bookId) { this.bookId = bookId; }
    public LocalDate getAddedDate() { return addedDate; }
    public void setAddedDate(LocalDate addedDate) { this.addedDate = addedDate; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public ReadStatus getReadStatus() { return readStatus; }
    public void setReadStatus(ReadStatus readStatus) { this.readStatus = readStatus; }
    public ReadingList getReadingList() { return readingList; }
    public void setReadingList(ReadingList readingList) { this.readingList = readingList; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Long id;
        private Long bookId;
        private LocalDate addedDate;
        private String notes;
        private ReadStatus readStatus = ReadStatus.TO_READ;
        private ReadingList readingList;

        public Builder id(Long id) { this.id = id; return this; }
        public Builder bookId(Long bookId) { this.bookId = bookId; return this; }
        public Builder addedDate(LocalDate addedDate) { this.addedDate = addedDate; return this; }
        public Builder notes(String notes) { this.notes = notes; return this; }
        public Builder readStatus(ReadStatus readStatus) { this.readStatus = readStatus; return this; }
        public Builder readingList(ReadingList readingList) { this.readingList = readingList; return this; }
        public ReadingListItem build() { return new ReadingListItem(id, bookId, addedDate, notes, readStatus, readingList); }
    }

    public enum ReadStatus {
        TO_READ, READING, COMPLETED
    }
}
