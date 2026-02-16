package com.library.catalog.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;

@Entity
@Table(name = "reading_list_items")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
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
    @Builder.Default
    private ReadStatus readStatus = ReadStatus.TO_READ;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reading_list_id", nullable = false)
    private ReadingList readingList;

    public enum ReadStatus {
        TO_READ, READING, COMPLETED
    }
}
