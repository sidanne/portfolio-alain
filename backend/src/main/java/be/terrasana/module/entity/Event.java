package be.terrasana.module.entity;

import be.terrasana.module.entity.enums.EventStatus;
import be.terrasana.module.entity.enums.RegistrationStatus;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Événement — dictionnaire de données section 5.2, table "events".
 * RG-05 : date, lieu et nombre maximum de participants obligatoires.
 */
@Entity
@Table(name = "events")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Event {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "admin_id")
    private Admin admin;

    @Column(nullable = false, length = 200)
    private String title;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String description;

    @Column(nullable = false)
    private LocalDateTime eventDate;

    @Column(nullable = false, length = 300)
    private String location;

    @Column(nullable = false)
    private Integer maxPlaces;

    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    private EventStatus status = EventStatus.OPEN;

    private String imageUrl;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @OneToMany(mappedBy = "event")
    private List<Registration> registrations = new ArrayList<>();

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }

    /** Places encore disponibles = maxPlaces - inscriptions CONFIRMED. */
    public int getAvailablePlaces() {
        long confirmed = registrations.stream()
                .filter(r -> r.getStatus() == RegistrationStatus.CONFIRMED)
                .count();
        return (int) Math.max(0, maxPlaces - confirmed);
    }

    /** RG-06 : passe à FULL dès que toutes les places CONFIRMED sont prises. */
    public boolean isFull() {
        return getAvailablePlaces() <= 0;
    }
}
