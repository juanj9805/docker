using vps.Data;
using vps.Models.Event;
using vps.Response;

namespace vps.Services;

public class EventService
{
    private readonly MysqlDbContext _context;

    public EventService(MysqlDbContext context)
    {
        _context = context;
    }
    
    public ServiceResponse <IEnumerable<Event>> GetAll()
    {
        var evs = _context.Events.ToList();

        return new ServiceResponse<IEnumerable<Event>>()
        {
            Data = evs,
            Message = "op",
            Succes = true,
        };
    }
}