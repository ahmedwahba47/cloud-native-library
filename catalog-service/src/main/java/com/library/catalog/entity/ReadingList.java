package com.library.catalog.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "reading_lists")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class ReadingList {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    private String description;

    @Column(name = "owner_name", nullable = false)
    private String ownerName;

    @Column(name = "created_date")
    private LocalDate createdDate;

    @OneToMany(mappedBy = "readingList", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
    @Builder.Default
    private List<ReadingListItem> items = new ArrayList<>();
}
