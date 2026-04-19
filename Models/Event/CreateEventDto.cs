using System.ComponentModel.DataAnnotations;

namespace vps.Models.Event;

public class CreateEventDto
{
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
}