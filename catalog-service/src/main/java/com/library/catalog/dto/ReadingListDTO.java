package com.library.catalog.dto;

import java.time.LocalDate;
import java.util.List;

public class ReadingListDTO {
    private Long id;
    private String name;
    private String description;
    private String ownerName;
    private LocalDate createdDate;
    private List<ReadingListItemDTO> items;

    public ReadingListDTO() {}

    public ReadingListDTO(Long id, String name, String description, String ownerName, LocalDate createdDate, List<ReadingListItemDTO> items) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.ownerName = ownerName;
        this.createdDate = createdDate;
        this.items = items;
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
    public List<ReadingListItemDTO> getItems() { return items; }
    public void setItems(List<ReadingListItemDTO> items) { this.items = items; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private Long id;
        private String name;
        private String description;
        private String ownerName;
        private LocalDate createdDate;
        private List<ReadingListItemDTO> items;

        public Builder id(Long id) { this.id = id; return this; }
        public Builder name(String name) { this.name = name; return this; }
        public Builder description(String description) { this.description = description; return this; }
        public Builder ownerName(String ownerName) { this.ownerName = ownerName; return this; }
        public Builder createdDate(LocalDate createdDate) { this.createdDate = createdDate; return this; }
        public Builder items(List<ReadingListItemDTO> items) { this.items = items; return this; }
        public ReadingListDTO build() { return new ReadingListDTO(id, name, description, ownerName, createdDate, items); }
    }
}
