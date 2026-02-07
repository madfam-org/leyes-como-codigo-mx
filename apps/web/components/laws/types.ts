export interface Law {
    official_id: string;
    name: string;
    category: string;
    tier: string;
    state: string | null;
    status?: string;
    last_verified?: string | null;
}

export interface LawVersion {
    publication_date: string | null;
    valid_from?: string;
    valid_to?: string | null;
    dof_url: string | null;
    change_summary?: string | null;
    xml_file?: string | null;
}

export interface Article {
    article_id: string;
    text: string;
    has_structure?: boolean;
}

export interface LawDetailData {
    law: Law;
    version: LawVersion;
    versions: LawVersion[];
    articles: Article[];
    total: number;
}
