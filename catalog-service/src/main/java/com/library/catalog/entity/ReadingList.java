package com.library.catalog.entity;

import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "reading_lists")
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
    private List<ReadingListItem> items = new ArrayList<>();

    public ReadingList() {}

    public ReadingList(Long id, String name, String description, String ownerName, LocalDate createdDate, List<ReadingListItem> items) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.ownerName = ownerName;
        this.createdDate = createdDate;
        this.items = items != null ? items : new ArrayList<>();
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }
    public LocalDate getCreatedDate() { return createdDate; }
    public void setCreatedDate(LocalDate createdDate) { this.createdDate = createdDate; }
    public List<ReadingListItem> getItems() { return items; }
    public void setItems(List<ReadingListItem> items) { this.items = items; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Long id;
        private String name;
        private String description;
        private String ownerName;
        private LocalDate createdDate;
        private List<ReadingListItem> items = new ArrayList<>();

        public Builder id(Long id) { this.id = id; return this; }
        public Builder name(String name) { this.name = name; return this; }
        public Builder description(String description) { this.description = description; return this; }
        public Builder ownerName(String ownerName) { this.ownerName = ownerName; return this; }
        public Builder createdDate(LocalDate createdDate) { this.createdDate = createdDate; return this; }
        public Builder items(List<ReadingListItem> items) { this.items = items; return this; }
        public ReadingList build() { return new ReadingList(id, name, description, ownerName, createdDate, items); }
    }
}
