package com.library.catalog.dto;

import jakarta.validation.constraints.NotBlank;

public class ReadingListCreateRequest {

    @NotBlank(message = "Name is required")
    private String name;

    private String description;

    @NotBlank(message = "Owner name is required")
    private String ownerName;

    public ReadingListCreateRequest() {}

    public ReadingListCreateRequest(String name, String description, String ownerName) {
        this.name = name;
        this.description = description;
        this.ownerName = ownerName;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private String name;
        private String description;
        private String ownerName;

        public Builder name(String name) { this.name = name; return this; }
        public Builder description(String description) { this.description = description; return this; }
        public Builder ownerName(String ownerName) { this.ownerName = ownerName; return this; }
        public ReadingListCreateRequest build() { return new ReadingListCreateRequest(name, description, ownerName); }
    }
}
