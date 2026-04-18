using System.ComponentModel.DataAnnotations;

namespace vps.Models.Event;

public enum Status {Active, Inactive, Deleted}

public class Event
{
    public int Id { get; set; }
    [Required]
    public string Title { get; set; } = string.Empty;
    [Required]
    public string Img { get; set; } = string.Empty;
    [Required]
    public string Description { get; set; } = string.Empty;
    [Required]
    public string Location { get; set; } = string.Empty;
    [Required]
    public Status Status { get; set; } = Status.Active;
    public DateTime CreateAt { get; set; } 
}